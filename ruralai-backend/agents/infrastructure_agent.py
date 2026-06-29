from typing import Dict, List, Any, Optional
import logging
import json
import re

class InfrastructureAgent:
    """Agent resolving public utility concerns (road quality, power grid, mobile reception, infrastructure plans)."""

    def __init__(self, llm_client: Any = None, llm_provider: Optional[str] = None):
        self.llm_client = llm_client
        self.llm_provider = llm_provider
        self.logger = logging.getLogger("InfrastructureAgent")

        # Mock Databases
        self.road_conditions_database: Dict[str, Dict[str, Any]] = {
            "pune": {"condition": "Fair", "potholes": "Moderate", "maintenance": "Scheduled in Sept 2026", "quality_rating": 6.5},
            "mysore": {"condition": "Good", "potholes": "Low", "maintenance": "Completed in Jan 2026", "quality_rating": 8.2},
            "jaipur": {"condition": "Poor", "potholes": "Severe", "maintenance": "Urgent review required", "quality_rating": 3.4},
            "amritsar": {"condition": "Good", "potholes": "Low", "maintenance": "Completed in May 2026", "quality_rating": 8.5}
        }
        
        self.electricity_status_database: Dict[str, Dict[str, Any]] = {
            "pune": {"average_supply_hours": 20, "load_shedding_schedule": "2 PM - 4 PM daily", "grid_stability": "Stable"},
            "mysore": {"average_supply_hours": 22, "load_shedding_schedule": "None", "grid_stability": "High"},
            "jaipur": {"average_supply_hours": 14, "load_shedding_schedule": "6 AM - 10 AM daily", "grid_stability": "Fluctuating"},
            "amritsar": {"average_supply_hours": 24, "load_shedding_schedule": "None", "grid_stability": "High"}
        }
        
        self.network_coverage_database: Dict[str, Dict[str, Any]] = {
            "pune": {"Jio": "4G/5G (Strong)", "Airtel": "4G (Strong)", "BSNL": "3G (Moderate)"},
            "mysore": {"Jio": "4G (Strong)", "Airtel": "4G/5G (Strong)", "BSNL": "3G/4G (Moderate)"},
            "jaipur": {"Jio": "4G (Moderate)", "Airtel": "4G (Poor)", "BSNL": "2G (Weak)"},
            "amritsar": {"Jio": "4G/5G (Strong)", "Airtel": "4G/5G (Strong)", "BSNL": "4G (Moderate)"}
        }
        
        self.government_projects_database: Dict[str, List[Dict[str, Any]]] = {
            "maharashtra": [
                {"project_name": "PMGSY - Shirur Rural Roads link", "authority": "NHAI / PWD", "status": "In Progress (65% Complete)", "completion_target": "Dec 2026"},
                {"project_name": "PMAY-G - Shirur Housing Development", "authority": "Ministry of Rural Development", "status": "Approved", "completion_target": "June 2027"}
            ],
            "karnataka": [
                {"project_name": "PMAY-G - Mysore Block Housing Scheme", "authority": "State Housing Corporation", "status": "In Progress (40% Complete)", "completion_target": "April 2027"}
            ],
            "rajasthan": [
                {"project_name": "PMGSY - Jodhpur Highway Expansion", "authority": "PWD", "status": "Delayed due to funds", "completion_target": "March 2027"}
            ],
            "punjab": [
                {"project_name": "Smart Village Development, Amritsar", "authority": "Panchayat Board", "status": "Completed", "completion_target": "Completed in May 2026"}
            ]
        }

    async def process(self, query: str, language: str = "hi") -> Dict[str, Any]:
        """Process user's infrastructure query. Lookup mock databases, formulate recommendations."""
        self.logger.info(f"InfrastructureAgent processing query: '{query}'")
        
        parsed = await self._parse_infrastructure_parameters(query)
        intent = parsed.get("intent", "government_projects")
        district = parsed.get("district", "Pune")
        state = parsed.get("state", "Maharashtra")
        provider = parsed.get("provider", "Jio")

        recommendations = []
        sources = ["InfrastructureDatabase"]

        try:
            dist_key = district.lower().strip()
            state_key = state.lower().strip()

            # Find closest key matching the mock database
            matched_dist = "pune"
            for k in self.road_conditions_database.keys():
                if k in dist_key:
                    matched_dist = k
                    break

            matched_state = "maharashtra"
            for k in self.government_projects_database.keys():
                if k in state_key:
                    matched_state = k
                    break

            if intent == "road_status" or any(w in query.lower() for w in ["road", "pothole", "highway", "path"]):
                road_info = self.road_conditions_database.get(matched_dist, self.road_conditions_database["pune"])
                desc = (
                    f"Road condition in {matched_dist.title()} district: **{road_info['condition']}**. "
                    f"Potholes frequency: {road_info['potholes']}. "
                    f"Quality Rating: {road_info['quality_rating']}/10. "
                    f"Maintenance schedule: {road_info['maintenance']}."
                )
                recommendations.append({
                    "title": f"PWD Road Quality Assessment: {matched_dist.title()}",
                    "description": desc,
                    "source": "Local PWD Survey Report",
                    "confidence": 0.80
                })

            elif intent == "electricity_supply" or any(w in query.lower() for w in ["electricity", "power", "grid", "load shedding", "voltage"]):
                power_info = self.electricity_status_database.get(matched_dist, self.electricity_status_database["pune"])
                desc = (
                    f"Electricity supply in {matched_dist.title()}: Average of **{power_info['average_supply_hours']} hours** per day. "
                    f"Scheduled load-shedding: {power_info['load_shedding_schedule']}. "
                    f"Grid voltage stability: {power_info['grid_stability']}."
                )
                recommendations.append({
                    "title": f"State Electricity Board Grid status: {matched_dist.title()}",
                    "description": desc,
                    "source": "State Power Distribution Corporation",
                    "confidence": 0.85
                })

            elif intent == "mobile_coverage" or any(w in query.lower() for w in ["coverage", "signal", "range", "mobile", "sim", "tower"]):
                coverage_info = self.network_coverage_database.get(matched_dist, self.network_coverage_database["pune"])
                desc = f"Mobile network coverage in {matched_dist.title()} district: "
                providers = []
                for prov, strength in coverage_info.items():
                    providers.append(f"{prov}: {strength}")
                desc += ", ".join(providers) + "."
                
                recommendations.append({
                    "title": f"Telecom Tower Signal Assessment: {matched_dist.title()}",
                    "description": desc,
                    "source": "Telecom Regulatory Data",
                    "confidence": 0.88
                })

            else:
                # Default: Government Projects
                projects = self.government_projects_database.get(matched_state, self.government_projects_database["maharashtra"])
                
                desc_lines = []
                for p in projects:
                    desc_lines.append(f"- **{p['project_name']}** (Authority: {p['authority']}): Status: {p['status']}. Expected Completion: {p['completion_target']}")
                    
                recommendations.append({
                    "title": f"Central & State Government Development Projects in {matched_state.title()}",
                    "description": "\n".join(desc_lines) if desc_lines else "No major rural infrastructure development projects logged.",
                    "source": "Rural Development Dashboard",
                    "confidence": 0.90
                })

        except Exception as e:
            self.logger.error(f"Error compiling recommendations: {e}")
            recommendations.append({
                "title": "Rural Utility Systems Support Error",
                "description": "Unable to execute public utility checks. Please check location parameters and try again.",
                "source": "InfrastructureAgent",
                "confidence": 0.50
            })

        return {
            "agent": "infrastructure",
            "recommendations": recommendations,
            "sources": list(set(sources))
        }

    async def _parse_infrastructure_parameters(self, query: str) -> Dict[str, Any]:
        """Extract geographic and provider details from query using LLM or rule-based fallback."""
        params = {
            "intent": "government_projects",
            "district": "Pune",
            "state": "Maharashtra",
            "provider": "Jio"
        }
        
        ql = query.lower()
        
        # Check intents
        if any(w in ql for w in ["road", "pothole", "highway", "tar"]):
            params["intent"] = "road_status"
        elif any(w in ql for w in ["electricity", "power", "grid", "shedding", "load", "voltage"]):
            params["intent"] = "electricity_supply"
        elif any(w in ql for w in ["coverage", "signal", "range", "mobile", "network", "sim", "tower"]):
            params["intent"] = "mobile_coverage"

        if self.llm_client:
            prompt = (
                "Extract infrastructure query parameters from this user query. Return a valid JSON object matching this schema:\n"
                '{"intent": "road_status"|"electricity_supply"|"mobile_coverage"|"government_projects", '
                '"district": "string (Indian district e.g. Pune, Jodhpur, Amritsar)", '
                '"state": "string (Indian state e.g. Punjab, Maharashtra)", '
                '"provider": "Jio"|"Airtel"|"BSNL"}\n'
                f"Query: '{query}'"
            )
            try:
                if self.llm_provider == "google":
                    response = self.llm_client.generate_content(prompt)
                    data = json.loads(re.sub(r'```json|```', '', response.text).strip())
                    params.update({k: v for k, v in data.items() if v})
                elif self.llm_provider == "anthropic":
                    response = await self.llm_client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=250,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    content_text = response.content[0].text
                    data = json.loads(re.sub(r'```json|```', '', content_text).strip())
                    params.update({k: v for k, v in data.items() if v})
                return params
            except Exception as e:
                self.logger.warning(f"LLM extraction failed, using fallback regex parser: {e}")

        # Fallback regex parser
        districts = ["pune", "mysore", "jaipur", "amritsar", "jodhpur", "satara"]
        for d in districts:
            if d in ql:
                params["district"] = d.title()
                break
                
        states = ["maharashtra", "karnataka", "rajasthan", "punjab"]
        for s in states:
            if s in ql:
                params["state"] = s.title()
                break
                
        providers = ["jio", "airtel", "bsnl"]
        for p in providers:
            if p in ql:
                params["provider"] = p.upper() if p != "airtel" else "Airtel"
                break
                
        return params
