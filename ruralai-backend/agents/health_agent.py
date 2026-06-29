from typing import Dict, List, Any, Optional
import logging
import json
import re
from mcp_servers.health_mcp import HealthMCPServer

class HealthAgent:
    """Agent resolving health concerns, hospital location queries, vaccination schedules, and dietary tips."""

    def __init__(self, health_mcp: HealthMCPServer, llm_client: Any = None, llm_provider: Optional[str] = None):
        self.health_mcp = health_mcp
        self.llm_client = llm_client
        self.llm_provider = llm_provider
        self.logger = logging.getLogger("HealthAgent")

    async def process(self, query: str, language: str = "hi") -> Dict[str, Any]:
        """Process user's health query. Detect parameters, trigger health MCP actions, compile recommendations."""
        self.logger.info(f"HealthAgent processing query: '{query}'")
        
        parsed = await self._parse_health_parameters(query)
        intent = parsed.get("intent", "disease_info")
        disease = parsed.get("disease", "fever")
        age = parsed.get("age", 30)
        gender = parsed.get("gender", "male")
        state = parsed.get("state", "Maharashtra")
        district = parsed.get("district")
        lat = parsed.get("lat", 18.5204)
        lon = parsed.get("lon", 73.8567)

        recommendations = []
        sources = ["HealthMCPServer"]

        try:
            if intent == "hospital_finder" or any(w in query.lower() for w in ["hospital", "clinic", "doctor", "emergency", "treatment center"]):
                hospitals = await self.health_mcp.find_nearby_hospitals(lat, lon, radius_km=50)
                sources.append("HealthMCPServer (Geographic Hospital Search)")
                
                desc_lines = []
                for h in hospitals:
                    desc_lines.append(f"- {h['name']} ({h['distance_km']} km away): Beds: {h['beds']}, Specialties: {', '.join(h['specialties'])}, 24h Emergency: {'Yes' if h['emergency_24h'] else 'No'}")
                
                recommendations.append({
                    "title": f"Nearby Government Health Centers (within 50km radius)",
                    "description": "\n".join(desc_lines) if desc_lines else "No government healthcare facilities found within 50km.",
                    "source": "HealthMCP",
                    "confidence": 0.95
                })

            elif intent == "vaccination_info" or any(w in query.lower() for w in ["vaccine", "vaccination", "polio", "bcg", "immunization", "baby dose"]):
                # Convert age to months (rough estimate if in years)
                age_months = age
                if age_months > 120:  # If age looks like years, convert or cap
                    age_months = int(age_months / 12)
                schedule = await self.health_mcp.get_vaccination_schedule(age_months)
                sources.append("HealthMCPServer (National Immunization Program)")
                
                desc_lines = []
                for s in schedule:
                    desc_lines.append(f"- {s['vaccine']} (Recommended around {s['age_days']} days old). Protects from: {s['disease']}. Dose: {s['dose']}")
                    
                recommendations.append({
                    "title": f"Immunization Tracker for Child ({age_months} Months)",
                    "description": "\n".join(desc_lines),
                    "source": "HealthMCP",
                    "confidence": 0.90
                })

            elif intent == "health_camps" or any(w in query.lower() for w in ["camp", "health camp", "free checkup", "medical checkup"]):
                camps = await self.health_mcp.find_health_camps(state, district)
                sources.append("HealthMCPServer (Rural Outreach Calendar)")
                
                desc_lines = []
                for c in camps:
                    desc_lines.append(f"- {c['camp_name']} at {c['location']} on {c['date']}. Services: {', '.join(c['services'])}")
                    
                recommendations.append({
                    "title": f"Upcoming Free Health Camps in {state.title()}",
                    "description": "\n".join(desc_lines),
                    "source": "HealthMCP",
                    "confidence": 0.85
                })

            elif intent == "nutrition_advice" or any(w in query.lower() for w in ["diet", "food", "nutrition", "eat", "protein", "energy"]):
                nut = await self.health_mcp.get_nutrition_advice(age, gender)
                sources.append("HealthMCPServer (Dietary Intake Standard)")
                
                recommendations.append({
                    "title": f"Dietary & Nutritional Plan for {age}yo {gender.title()}",
                    "description": f"Daily Caloric Requirement: {nut['daily_calories']}. Key Nutrients: {nut['macronutrients']}. Recommendations: {nut['practical_advice']}",
                    "source": "HealthMCP",
                    "confidence": 0.90
                })

            else:
                # Default: Disease Reference Info
                dis = await self.health_mcp.get_disease_info(disease)
                sources.append("HealthMCPServer (Clinical Definition Guide)")
                
                recommendations.append({
                    "title": f"Health Care Guide: {dis['name'].title()}",
                    "description": f"Common Symptoms: {', '.join(dis['symptoms'])}. At-Home Treatment: {dis['treatment']}. Clinical Alert: {dis['when_to_see_doctor']}",
                    "source": "HealthMCP",
                    "confidence": 0.92
                })

        except Exception as e:
            self.logger.error(f"Error compiling recommendations: {e}")
            recommendations.append({
                "title": "Medical Intelligence Issue",
                "description": "Unable to load health parameters. Please visit the nearest Primary Health Center (PHC) for direct clinical support.",
                "source": "HealthAgent",
                "confidence": 0.50
            })

        return {
            "agent": "health",
            "recommendations": recommendations,
            "sources": list(set(sources))
        }

    async def _parse_health_parameters(self, query: str) -> Dict[str, Any]:
        """Extract medical attributes (disease, age, gender, coordinates, state) from query."""
        params = {
            "intent": "disease_info",
            "disease": "fever",
            "age": 30,
            "gender": "male",
            "state": "Maharashtra",
            "district": None,
            "lat": 18.5204,
            "lon": 73.8567
        }
        
        ql = query.lower()
        
        # Detect intent
        if any(w in ql for w in ["hospital", "clinic", "doctor", "emergency", "medicine shop"]):
            params["intent"] = "hospital_finder"
        elif any(w in ql for w in ["vaccine", "vaccination", "polio", "bcg", "immunization", "injection"]):
            params["intent"] = "vaccination_info"
        elif any(w in ql for w in ["camp", "health camp", "free checkup", "eye check"]):
            params["intent"] = "health_camps"
        elif any(w in ql for w in ["diet", "food", "nutrition", "eat", "growth", "protein"]):
            params["intent"] = "nutrition_advice"

        # Ask LLM if client configured
        if self.llm_client:
            prompt = (
                "Extract health parameters from this user query. Return a valid JSON object matching this schema:\n"
                '{"intent": "hospital_finder"|"vaccination_info"|"health_camps"|"nutrition_advice"|"disease_info", '
                '"disease": "string (e.g. malaria, fever, headache, diabetes)", "age": integer, '
                '"gender": "male"|"female"|"child", "state": "string (Indian state)", '
                '"district": "string (Indian district)", "lat": float, "lon": float}\n'
                f"Query: '{query}'"
            )
            try:
                if self.llm_provider == "google":
                    response = self.llm_client.generate_content(prompt)
                    data = json.loads(re.sub(r'```json|```', '', response.text).strip())
                    params.update({k: v for k, v in data.items() if v is not None})
                elif self.llm_provider == "anthropic":
                    response = await self.llm_client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=250,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    content_text = response.content[0].text
                    data = json.loads(re.sub(r'```json|```', '', content_text).strip())
                    params.update({k: v for k, v in data.items() if v is not None})
                return params
            except Exception as e:
                self.logger.warning(f"LLM extraction failed, using fallback regex parser: {e}")

        # Regex fallback parser
        diseases = ["fever", "diarrhea", "malaria", "cough", "cold", "headache", "cholera", "typhoid"]
        for d in diseases:
            if d in ql:
                params["disease"] = d
                break
                
        if "female" in ql or "woman" in ql or "girl" in ql:
            params["gender"] = "female"
        elif "child" in ql or "baby" in ql or "infant" in ql:
            params["gender"] = "child"
            params["age"] = 1
            
        states = ["maharashtra", "karnataka", "tamil nadu", "rajasthan", "punjab"]
        for s in states:
            if s in ql:
                params["state"] = s.title()
                break

        # Check for ages using regex
        age_match = re.search(r'\b(\d+)\s*(year|yr|month|mth|yo)\b', ql)
        if age_match:
            params["age"] = int(age_match.group(1))
            if age_match.group(2) in ["month", "mth"]:
                params["intent"] = "vaccination_info"
                
        return params
