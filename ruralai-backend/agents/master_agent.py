from typing import Dict, List, Any, Optional
import json
import logging
from datetime import datetime
from config.settings import settings
from utils.response_formatter import format_agent_response

class MasterAgent:
    """Master orchestrator that classifies user queries, routes them to domain agents, and aggregates results."""

    def __init__(self):
        self.logger = logging.getLogger("MasterAgent")

        # Initialize MCP Servers
        from mcp_servers.weather_mcp import WeatherMCPServer
        from mcp_servers.agriculture_mcp import AgricultureMCPServer
        from mcp_servers.health_mcp import HealthMCPServer
        from mcp_servers.education_mcp import EducationMCPServer
        from mcp_servers.water_mcp import WaterMCPServer
        from mcp_servers.finance_mcp import FinanceMCPServer

        self.weather_mcp = WeatherMCPServer(api_key=settings.openweather_api_key)
        self.agriculture_mcp = AgricultureMCPServer()
        self.health_mcp = HealthMCPServer()
        self.education_mcp = EducationMCPServer()
        self.water_mcp = WaterMCPServer()
        self.finance_mcp = FinanceMCPServer()

        self.agents_map = {
            "agriculture": "AgricultureAgent",
            "health": "HealthAgent",
            "education": "EducationAgent",
            "water": "WaterAgent",
            "infrastructure": "InfrastructureAgent",
            "finance": "FinanceAgent"
        }

        # Initialize LLM Integration
        self.llm_client = None
        self.llm_provider = None

        if settings.google_api_key and settings.google_api_key != "dummy_google_key":
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.google_api_key)
                self.llm_client = genai.GenerativeModel('gemini-pro')
                self.llm_provider = "google"
                self.logger.info("MasterAgent configured with Google Gemini Pro.")
            except Exception as e:
                self.logger.warning(f"Failed to load Google Generative AI client: {e}")

        # Anthropic configuration removed as requested

    async def process_query(self, query: str, category: Optional[str] = None, language: str = "hi") -> Dict[str, Any]:
        """Orchestrate query categorization, domain delegation, formatting, and translation."""
        start_time = datetime.now()
        self.logger.info(f"Query incoming: '{query}' in language: {language}")

        # 1. Infer category if missing
        if not category or category == "string" or category.lower().strip() not in self.agents_map:
            category = await self._route_query(query)
            self.logger.info(f"Routed category inferred: {category}")
        else:
            category = category.lower().strip()

        # 2. Dispatch to domain agent
        try:
            agent = self._get_agent(category)
            agent_response = await agent.process(query, language)
            
            # Embed metadata
            processing_time = (datetime.now() - start_time).total_seconds()
            agent_response["processing_time"] = processing_time
            
            # 3. Format and translate final response
            formatted = self._format_response(agent_response, language)
            return formatted

        except Exception as e:
            self.logger.exception("Error processing agent query execution")
            processing_time = (datetime.now() - start_time).total_seconds()
            return {
                "query_id": "error-fallback",
                "agent_used": category,
                "recommendations": [
                    {
                        "title": "Query Processing Error",
                        "description": "An unexpected error occurred while resolving your request. Please try again later.",
                        "source": "MasterAgent",
                        "confidence": 0.0
                    }
                ],
                "sources": ["System Exception Handler"],
                "language": language,
                "processing_time": processing_time,
                "timestamp": datetime.utcnow().isoformat(),
                "message": f"Execution failed: {str(e)}"
            }

    async def _route_query(self, query: str) -> str:
        """Categorize a query into a target domain using LLM or rule-based keyword mapping."""
        query_clean = query.lower().strip()

        # Rule-based fallback keywords mapping
        keywords = {
            "agriculture": ["crop", "soil", "tomato", "fertilizer", "pest", "mandi", "farming", "harvest", "seed", "disease", "yield", "urea", "potash"],
            "health": ["fever", "hospital", "doctor", "medicine", "vaccine", "camp", "diet", "nutrition", "pain", "pregnancy", "illness", "symptom", "baby"],
            "education": ["school", "college", "scholarship", "exam", "grade", "admission", "study", "career", "guidance", "teacher", "document"],
            "water": ["groundwater", "borewell", "bore well", "harvesting", "well", "drinking water", "irrigation", "water quality", "depth", "rainwater"],
            "infrastructure": ["road", "electricity", "power", "coverage", "signal", "tower", "construction", "network", "project", "telecom"],
            "finance": ["loan", "emi", "subsidy", "scheme", "savings", "bank", "pm-kisan", "interest", "finance", "kcc", "subsidies"]
        }

        # Attempt LLM classification
        if self.llm_client:
            prompt = (
                "You are the orchestrator router for RuralAI. Classify this user query into exactly one of "
                "these categories: agriculture, health, education, water, infrastructure, finance.\n"
                f"Query: '{query}'\n"
                "Response: Return only the category name in lowercase and nothing else."
            )
            try:
                if self.llm_provider == "google":
                    response = self.llm_client.generate_content(prompt)
                    category = response.text.strip().lower()
                    if category in self.agents_map:
                        return category
                pass
            except Exception as e:
                self.logger.warning(f"LLM routing failed, using rule-based classifier: {e}")

        # Rule-based fallback classifier
        scores = {cat: 0 for cat in keywords}
        for cat, words in keywords.items():
            for w in words:
                if w in query_clean:
                    scores[cat] += 2  # Boost exact keyword matches
        
        best_cat = max(scores, key=scores.get)
        if scores[best_cat] > 0:
            return best_cat

        return "agriculture"

    def _get_agent(self, category: str) -> Any:
        """Resolve and instantiate the specific agent for the given category."""
        if category == "agriculture":
            from agents.agriculture_agent import AgricultureAgent
            return AgricultureAgent(self.agriculture_mcp, self.weather_mcp, self.llm_client, self.llm_provider)
        elif category == "health":
            from agents.health_agent import HealthAgent
            return HealthAgent(self.health_mcp, self.llm_client, self.llm_provider)
        elif category == "education":
            from agents.education_agent import EducationAgent
            return EducationAgent(self.education_mcp, self.llm_client, self.llm_provider)
        elif category == "water":
            from agents.water_agent import WaterAgent
            return WaterAgent(self.water_mcp, self.weather_mcp, self.llm_client, self.llm_provider)
        elif category == "infrastructure":
            from agents.infrastructure_agent import InfrastructureAgent
            return InfrastructureAgent(self.llm_client, self.llm_provider)
        elif category == "finance":
            from agents.finance_agent import FinanceAgent
            return FinanceAgent(self.finance_mcp, self.llm_client, self.llm_provider)
        else:
            raise ValueError(f"Unknown category: {category}")

    def _format_response(self, agent_response: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Perform formatting and translations for the outgoing payload."""
        import uuid
        query_id = str(uuid.uuid4())
        
        # Invoke standard translation and schema format utility
        formatted_data = format_agent_response(agent_response, language)
        
        return {
            "query_id": query_id,
            "agent_used": formatted_data.get("agent", "unknown"),
            "recommendations": formatted_data.get("recommendations", []),
            "sources": formatted_data.get("sources", []),
            "language": language,
            "processing_time": agent_response.get("processing_time", 0.0),
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Query completed successfully"
        }
