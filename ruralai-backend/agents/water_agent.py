from typing import Dict, List, Any, Optional
import logging
import json
import re
from mcp_servers.water_mcp import WaterMCPServer
from mcp_servers.weather_mcp import WeatherMCPServer

class WaterAgent:
    """Agent resolving water level monitoring, water harvesting schemes, quality tests, and drilling locations."""

    def __init__(self, water_mcp: WaterMCPServer, weather_mcp: WeatherMCPServer, llm_client: Any = None, llm_provider: Optional[str] = None):
        self.water_mcp = water_mcp
        self.weather_mcp = weather_mcp
        self.llm_client = llm_client
        self.llm_provider = llm_provider
        self.logger = logging.getLogger("WaterAgent")

    async def process(self, query: str, language: str = "hi") -> Dict[str, Any]:
        """Process user's water query. Identify intent, trigger water MCP, compile recommendations."""
        self.logger.info(f"WaterAgent processing query: '{query}'")
        
        parsed = await self._parse_water_parameters(query)
        intent = parsed.get("intent", "groundwater_level")
        lat = parsed.get("lat", 18.5204)
        lon = parsed.get("lon", 73.8567)
        soil_type = parsed.get("soil_type", "loamy")
        rainfall_mm = parsed.get("rainfall_mm", 750)
        region = parsed.get("region", "Maharashtra")
        source_type = parsed.get("source_type", "borewell")
        area_sqft = parsed.get("area_sqft", 1000)
        crop = parsed.get("crop", "tomato")

        recommendations = []
        sources = ["WaterMCPServer"]

        try:
            if intent == "bore_well_prediction" or any(w in query.lower() for w in ["borewell", "bore well", "drill", "dig"]):
                prediction = await self.water_mcp.predict_bore_well_depth(soil_type, rainfall_mm, region)
                sources.append("WaterMCPServer (Borewell Drilling Predictor)")
                
                desc = (
                    f"Optimal drilling depth estimate: **{prediction['predicted_bore_well_depth_meters']} meters** "
                    f"for {region.title()} ({soil_type} soil, {rainfall_mm}mm annual rainfall). "
                    f"Strike Success Probability: **{int(prediction['success_probability'] * 100)}%**. "
                    f"Recommendation: {prediction['drill_recommendation']}."
                )
                recommendations.append({
                    "title": f"Borewell Drilling Feasibility Analysis",
                    "description": desc,
                    "source": "WaterMCP",
                    "confidence": 0.85
                })

            elif intent == "water_quality" or any(w in query.lower() for w in ["quality", "ph", "tds", "drinking", "safe to drink", "clean", "dirty"]):
                quality = await self.water_mcp.get_water_quality(source_type, region)
                sources.append("WaterMCPServer (Hydrological Quality Database)")
                
                safety_str = "Safe for consumption" if quality["safe_for_drinking"] else "Not Safe for consumption without treatment"
                params = quality["parameters"]
                remediations = "; ".join(quality["remediation_steps"])
                
                desc = (
                    f"Source: {source_type.title()} in {region.title()}. Status: **{safety_str}**. "
                    f"Parameters - pH: {params['pH']}, TDS: {params['TDS_ppm']} ppm, Fluoride: {params['fluoride_mg_l']} mg/L. "
                    f"Action Steps: {remediations}."
                )
                recommendations.append({
                    "title": f"Water Quality Test Results: {source_type.title()}",
                    "description": desc,
                    "source": "WaterMCP",
                    "confidence": 0.90
                })

            elif intent == "rainwater_harvesting" or any(w in query.lower() for w in ["harvesting", "rainwater", "harvest", "save rain", "catchment"]):
                plan = await self.water_mcp.get_rainwater_harvesting_plan(rainfall_mm, area_sqft, region)
                sources.append("WaterMCPServer (Rainwater Engineering Guides)")
                
                techs = ", ".join(plan["techniques"])
                desc = (
                    f"Catchment Area: {area_sqft} sqft. Annual Rainfall: {rainfall_mm}mm. "
                    f"Harvestable Water Potential: **{plan['total_annual_run_off_liters']} Liters**. "
                    f"Recommended Tank Capacity: **{plan['recommended_tank_capacity_liters']} Liters** ({plan['recommended_system_type']} setup). "
                    f"Recommended Designs: {techs}. Estimated Cost: {plan['estimated_cost_inr'][0]}-{plan['estimated_cost_inr'][1]} INR. "
                    f"Maintenance: {plan['maintenance_guidelines']}."
                )
                recommendations.append({
                    "title": f"Domestic Rainwater Harvesting Design blueprint",
                    "description": desc,
                    "source": "WaterMCP",
                    "confidence": 0.88
                })

            elif intent == "irrigation_schedule" or any(w in query.lower() for w in ["irrigation", "irrigate", "water crop", "watering"]):
                # Call weather forecast to check local rains
                weather_data = await self.weather_mcp.get_forecast(lat, lon)
                forecast_rain = sum([day["rainfall_mm"] for day in weather_data["forecast"][:3]])  # Next 3 days rain
                
                schedule = await self.water_mcp.get_irrigation_schedule(crop, int(forecast_rain), soil_type)
                sources.append("WaterMCPServer (Irrigation Scheduler)")
                sources.append("WeatherMCPServer")
                
                desc = (
                    f"Crop: {crop.title()}. Soil: {soil_type}. Alert: {schedule['status'].replace('_', ' ').title()}. "
                    f"Water Required: {schedule['water_requirement_liters_per_plant_day']} Liters/plant/day. "
                    f"Drip Watering depth: {schedule['watering_depth_mm']}mm. "
                    f"Schedule: {schedule['recommended_frequency']}. Next watering should be in **{schedule['next_watering_in_days']} days**."
                )
                recommendations.append({
                    "title": f"Agronomic Irrigation Scheduling for {crop.title()}",
                    "description": desc,
                    "source": "WaterMCP + WeatherMCP",
                    "confidence": 0.90
                })

            else:
                # Default: Groundwater levels
                gw = await self.water_mcp.get_groundwater_level(lat, lon)
                sources.append("WaterMCPServer (State Hydrology Reports)")
                
                desc = (
                    f"Estimated Groundwater Table Depth: **{gw['average_depth_meters']} meters** "
                    f"in {gw['region_inferred']} region. Trend: {gw['trend'].title()}. "
                    f"Water Quality: {gw['water_quality'].title()}. "
                    f"Drilling Advisory: Minimum drilling depth should be {gw['recommended_drilling_depth_meters']} meters to hit stable aquifer."
                )
                recommendations.append({
                    "title": f"Regional Aquifer & Groundwater Assessment",
                    "description": desc,
                    "source": "WaterMCP",
                    "confidence": 0.92
                })

        except Exception as e:
            self.logger.error(f"Error compiling recommendations: {e}")
            recommendations.append({
                "title": "Water Hydrological System Error",
                "description": "Unable to perform water calculations. Ensure soil type, coordinate locations, or crop types are correctly set.",
                "source": "WaterAgent",
                "confidence": 0.50
            })

        return {
            "agent": "water",
            "recommendations": recommendations,
            "sources": list(set(sources))
        }

    async def _parse_water_parameters(self, query: str) -> Dict[str, Any]:
        """Extract hydrological attributes (soil, coordinates, region, area, crop) from query."""
        params = {
            "intent": "groundwater_level",
            "lat": 18.5204,
            "lon": 73.8567,
            "soil_type": "loamy",
            "rainfall_mm": 750,
            "region": "Maharashtra",
            "source_type": "borewell",
            "area_sqft": 1000,
            "crop": "tomato"
        }
        
        ql = query.lower()
        
        # Check intents
        if any(w in ql for w in ["borewell", "bore well", "drill", "dig"]):
            params["intent"] = "bore_well_prediction"
        elif any(w in ql for w in ["quality", "safe to drink", "clean", "dirty", "ph", "tds"]):
            params["intent"] = "water_quality"
        elif any(w in ql for w in ["harvesting", "rainwater", "harvest", "save rain"]):
            params["intent"] = "rainwater_harvesting"
        elif any(w in ql for w in ["irrigation", "irrigate", "water crop", "watering"]):
            params["intent"] = "irrigation_schedule"

        if self.llm_client:
            prompt = (
                "Extract water parameters from this user query. Return a valid JSON object matching this schema:\n"
                '{"intent": "groundwater_level"|"bore_well_prediction"|"water_quality"|"rainwater_harvesting"|"irrigation_schedule", '
                '"lat": float, "lon": float, "soil_type": "string (sandy, clayey, loamy, rocky)", '
                '"rainfall_mm": integer, "region": "string (Indian state or area)", '
                '"source_type": "borewell"|"well"|"river"|"pond", "area_sqft": integer, "crop": "string (crop name if mentioned)"}\n'
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

        # Fallback regex parser
        soils = ["sandy", "clayey", "loamy", "rocky"]
        for s in soils:
            if s in ql:
                params["soil_type"] = s
                break
                
        states = ["maharashtra", "karnataka", "tamil nadu", "rajasthan", "punjab"]
        for st in states:
            if st in ql:
                params["region"] = st.title()
                break
                
        crops = ["tomato", "wheat", "rice", "potato", "onion"]
        for cr in crops:
            if cr in ql:
                params["crop"] = cr
                break
                
        sources = ["borewell", "well", "river", "pond", "tap"]
        for src in sources:
            if src in ql:
                params["source_type"] = src
                break

        # Area extract (sqft)
        area_match = re.search(r'\b(\d+)\s*(sqft|sq\s*ft|square\s*feet|sq\.ft)\b', ql)
        if area_match:
            params["area_sqft"] = int(area_match.group(1))
            
        return params
