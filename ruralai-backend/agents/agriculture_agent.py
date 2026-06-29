from typing import Dict, List, Any, Optional
import logging
import re
from datetime import datetime
from mcp_servers.agriculture_mcp import AgricultureMCPServer
from mcp_servers.weather_mcp import WeatherMCPServer

class AgricultureAgent:
    """Agent resolving crop selection, disease identification, soil treatment, and market rates."""

    def __init__(self, agriculture_mcp: AgricultureMCPServer, weather_mcp: WeatherMCPServer, llm_client: Any = None, llm_provider: Optional[str] = None):
        self.agriculture_mcp = agriculture_mcp
        self.weather_mcp = weather_mcp
        self.llm_client = llm_client
        self.llm_provider = llm_provider
        self.logger = logging.getLogger("AgricultureAgent")

    async def process(self, query: str, language: str = "hi") -> Dict[str, Any]:
        """Process user's agriculture query. Parse intent, invoke MCP utilities, and compile recommendations."""
        self.logger.info(f"AgricultureAgent processing query: '{query}'")
        
        # 1. Parse intent and parameters using LLM or rule-based parser
        parsed = await self._parse_query_parameters(query)
        intent = parsed.get("intent", "crop_info")
        crop = parsed.get("crop", "tomato")
        state = parsed.get("state", "Maharashtra")
        soil_type = parsed.get("soil_type", "loamy")
        symptoms = parsed.get("symptoms", "")
        rainfall = parsed.get("rainfall", 600)
        
        recommendations = []
        sources = ["AgricultureMCPServer"]
        
        try:
            if intent == "disease_detection" or "disease" in query.lower() or "symptom" in query.lower():
                diseases = await self.agriculture_mcp.get_crop_diseases(crop)
                sources.append("AgricultureMCPServer (Disease Database)")
                for d in diseases:
                    recommendations.append({
                        "title": f"Disease Diagnosis: {d['disease_name'].title()} for {crop.title()}",
                        "description": (
                            f"Symptoms: {', '.join(d['symptoms'])}. "
                            f"Recommended Treatment: {d['treatment']}. "
                            f"Organic Option: {d['organic_solution']}. "
                            f"Prevention: {', '.join(d['prevention'])}."
                        ),
                        "source": "AgricultureMCP",
                        "confidence": 0.85
                    })

            elif intent == "fertilizer_recommendation" or "fertilizer" in query.lower() or "npk" in query.lower():
                fert = await self.agriculture_mcp.get_fertilizer_recommendation(crop, soil_type)
                sources.append("AgricultureMCPServer (Soil Fertilizer Matrix)")
                desc = f"Recommended Nutrient Ratio: {fert['recommended_npk_ratio']}. Suggested Products: "
                products = []
                for f in fert["fertilizers"]:
                    products.append(f"{f['name']} ({f['dosage_kg_per_hectare']} kg/ha, brands: {', '.join(f['brands'])})")
                desc += "; ".join(products)
                recommendations.append({
                    "title": f"Soil Nutrient & Fertilizer Plan for {crop.title()} in {soil_type} soil",
                    "description": desc,
                    "source": "AgricultureMCP",
                    "confidence": 0.90
                })

            elif intent == "market_prices" or "price" in query.lower() or "mandi" in query.lower() or "rate" in query.lower():
                prices = await self.agriculture_mcp.get_market_prices(crop, state)
                sources.append("AgricultureMCPServer (APMC Price Tracker)")
                mandi_info = "; ".join([f"{m['mandi_name']} ({m['distance_km']} km away): {m['price_per_kg']} INR/kg" for m in prices["nearest_mandis"]])
                recommendations.append({
                    "title": f"Market Price Alert: {crop.title()} in {state.title()}",
                    "description": f"Average Mandi price: {prices['average_price_per_kg']} INR/kg (Updated: {prices['last_updated']}). Nearest Mandis: {mandi_info}.",
                    "source": "AgricultureMCP",
                    "confidence": 0.95
                })

            elif intent == "yield_prediction" or "yield" in query.lower() or "produce" in query.lower():
                crop_info = await self.agriculture_mcp.get_crop_info(crop, state)
                sources.append("AgricultureMCPServer (Agronomy Database)")
                # Predict yield based on rain, soil and crop parameters
                base_yield = crop_info.get("expected_yield_tons_per_hectare", 10.0)
                # LLM based yields calculation or fallback
                yield_estimate = base_yield
                if "sandy" in soil_type.lower():
                    yield_estimate *= 0.85
                elif "clay" in soil_type.lower():
                    yield_estimate *= 0.95
                
                desc = f"Expected crop harvest yield: {round(yield_estimate, 1)} tons per hectare. Assumptions: standard weather and NPK dosage compliance."
                if self.llm_client:
                    desc = await self._generate_llm_summary(
                        f"Explain predicted yield for {crop} in {state} with {soil_type} soil under {rainfall}mm rainfall. Base yield is {base_yield}."
                    )
                recommendations.append({
                    "title": f"Yield Projection for {crop.title()} in {state.title()}",
                    "description": desc,
                    "source": "AgricultureMCP + LLM Estimator",
                    "confidence": 0.75
                })

            else:
                # Default: Crop selection and weather suitability
                # Get coordinates based on state
                lat, lon = self._get_state_coordinates(state)
                weather_data = await self.weather_mcp.get_forecast(lat, lon)
                crop_info = await self.agriculture_mcp.get_crop_info(crop, state)
                impact = await self.agriculture_mcp.get_weather_impact(crop, weather_data)
                
                sources.append("WeatherMCPServer")
                sources.append("AgricultureMCPServer (Agronomy Database)")
                
                status_str = "favorable" if impact["overall_status"] == "favorable" else "risky"
                desc = (
                    f"Crop Season: {crop_info.get('season')}. Water Required: {crop_info.get('water_need_mm')}mm. "
                    f"15-Day Rainfall: {impact['total_rainfall_forecasted_mm']}mm. "
                    f"Weather Status: The upcoming forecast is {status_str} for sowing {crop}. "
                    f"Warnings: {', '.join(impact['warnings'])}."
                )
                recommendations.append({
                    "title": f"Crop Sowing Suitability: {crop.title()} in {state.title()}",
                    "description": desc,
                    "source": "AgricultureMCP + WeatherMCP",
                    "confidence": 0.88
                })

        except Exception as e:
            self.logger.error(f"Error compiling recommendations: {e}")
            recommendations.append({
                "title": "Data Retrievable Issue",
                "description": f"Unable to fetch specific metrics for {crop}. Check spelling and region parameters.",
                "source": "AgricultureAgent",
                "confidence": 0.50
            })
            
        return {
            "agent": "agriculture",
            "recommendations": recommendations,
            "sources": list(set(sources))
        }

    async def _parse_query_parameters(self, query: str) -> Dict[str, Any]:
        """Extract agronomic entities (crop, state, soil, symptoms) from query text."""
        params = {
            "intent": "crop_info",
            "crop": "tomato",
            "state": "Maharashtra",
            "soil_type": "loamy",
            "symptoms": "",
            "rainfall": 600
        }
        
        # Check for intent keywords
        ql = query.lower()
        if any(w in ql for w in ["disease", "spot", "blight", "fungus", "mold", "symptom"]):
            params["intent"] = "disease_detection"
        elif any(w in ql for w in ["fertilizer", "urea", "potash", "dap", "npk", "manure"]):
            params["intent"] = "fertilizer_recommendation"
        elif any(w in ql for w in ["price", "mandi", "rate", "cost", "market"]):
            params["intent"] = "market_prices"
        elif any(w in ql for w in ["yield", "harvest", "produce", "ton"]):
            params["intent"] = "yield_prediction"
            
        # Try to use LLM parsing if client exists
        if self.llm_client:
            prompt = (
                "Extract query variables from this Indian rural query. Return a valid JSON object matching this schema:\n"
                '{"intent": "disease_detection"|"fertilizer_recommendation"|"market_prices"|"yield_prediction"|"crop_info", '
                '"crop": "string (e.g. wheat, rice, tomato)", "state": "string (Indian state e.g. Punjab, Maharashtra)", '
                '"soil_type": "string (e.g. sandy, clayey, loamy)", "symptoms": "string (symptoms described)"}\n'
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
                self.logger.warning(f"LLM entity extraction failed. Using fallback regex parser: {e}")

        # Regex fallback parser
        crops = ["tomato", "wheat", "rice", "potato", "sugarcane", "cotton", "maize", "onion"]
        for c in crops:
            if c in ql:
                params["crop"] = c
                break
                
        states = ["maharashtra", "karnataka", "punjab", "haryana", "tamil nadu", "gujarat", "rajasthan"]
        for s in states:
            if s in ql:
                params["state"] = s.title()
                break
                
        soils = ["sandy", "clayey", "loamy", "black", "red"]
        for sl in soils:
            if sl in ql:
                params["soil_type"] = sl
                break
                
        return params

    def _get_state_coordinates(self, state: str) -> tuple:
        """Helper to get coordinates for state capitals to map weather forecasts."""
        coords = {
            "Maharashtra": (18.5204, 73.8567), # Pune
            "Karnataka": (12.9716, 77.5946), # Bangalore
            "Punjab": (30.7333, 76.7794), # Chandigarh
            "Tamil Nadu": (13.0827, 80.2707), # Chennai
            "Rajasthan": (26.9124, 75.7873), # Jaipur
            "Gujarat": (23.2156, 72.6369) # Gandhinagar
        }
        return coords.get(state.title().strip(), (18.5204, 73.8567))

    async def _generate_llm_summary(self, prompt: str) -> str:
        """Internal helper to ask LLM for summary insights."""
        try:
            if self.llm_provider == "google":
                return self.llm_client.generate_content(prompt).text.strip()
            elif self.llm_provider == "anthropic":
                res = await self.llm_client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                return res.content[0].text.strip()
        except Exception as e:
            self.logger.error(f"Failed to generate LLM summary: {e}")
        return "Prediction complete based on static rural agronomy averages."
