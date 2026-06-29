from typing import Dict, List, Any
import logging

class WaterMCPServer:
    """MCP Server providing groundwater tracking, borewell analysis, and water harvesting planning."""

    def __init__(self):
        self.logger = logging.getLogger("WaterMCPServer")

        # 1. Groundwater Database by State
        self.groundwater_database: Dict[str, Dict[str, Any]] = {
            "maharashtra": {
                "average_depth_meters": 45.0,
                "trend": "declining",  # declining / stable / improving
                "quality": "good",      # good / moderate / poor
                "recommended_depth_meters": 50.0
            },
            "karnataka": {
                "average_depth_meters": 65.0,
                "trend": "declining",
                "quality": "moderate",
                "recommended_depth_meters": 75.0
            },
            "rajasthan": {
                "average_depth_meters": 110.0,
                "trend": "declining",
                "quality": "moderate",
                "recommended_depth_meters": 130.0
            },
            "punjab": {
                "average_depth_meters": 35.0,
                "trend": "declining",
                "quality": "good",
                "recommended_depth_meters": 45.0
            },
            "tamil nadu": {
                "average_depth_meters": 55.0,
                "trend": "stable",
                "quality": "good",
                "recommended_depth_meters": 60.0
            },
            "gujarat": {
                "average_depth_meters": 50.0,
                "trend": "improving",
                "quality": "moderate",
                "recommended_depth_meters": 55.0
            }
        }
        # Fallback list of other states to cover all states
        all_states = ["uttar pradesh", "madhya pradesh", "bihar", "west bengal", "andhra pradesh", 
                      "telangana", "kerala", "odisha", "assam", "haryana", "himachal pradesh"]
        for st in all_states:
            self.groundwater_database[st] = {
                "average_depth_meters": 40.0,
                "trend": "stable",
                "quality": "good",
                "recommended_depth_meters": 45.0
            }

        # 2. Rainwater Harvesting Guides Database
        self.rainwater_harvesting_guides: Dict[str, Dict[str, Any]] = {
            "semi_arid": {
                "techniques": ["Rooftop collection tank system", "Recharge pit with filter media", "Farm check dam"],
                "tank_capacity_liters": 50000,
                "cost_range_inr": [100000, 200000],
                "maintenance": "Clean rooftop mesh monthly. Flush filter media before monsoon."
            },
            "hilly": {
                "techniques": ["Contour trenching", "Spring-back storage tanks", "Bamboo piping streams"],
                "tank_capacity_liters": 20000,
                "cost_range_inr": [40000, 90000],
                "maintenance": "Keep intake channels free from dry leaves and silt deposits."
            },
            "plains": {
                "techniques": ["Percolation ponds", "Recharge wells", "Borewell casing recharge"],
                "tank_capacity_liters": 80000,
                "cost_range_inr": [80000, 150000],
                "maintenance": "Clean sedimentation trap twice a year. Keep bypass valves operational."
            }
        }

    async def get_groundwater_level(self, lat: float, lon: float) -> Dict[str, Any]:
        """Fetch estimated groundwater depth, trend, and chemical quality parameters for a coordinate."""
        self.logger.info(f"Retrieving groundwater level for lat: {lat}, lon: {lon}")
        
        # Simple coordinate bounds mapping to states
        # Default fallback is Maharashtra
        state_key = "maharashtra"
        if 11.0 <= lat <= 15.0 and 74.0 <= lon <= 79.0:
            state_key = "karnataka"
        elif 24.0 <= lat <= 30.0 and 69.0 <= lon <= 78.0:
            state_key = "rajasthan"
        elif 30.0 <= lat <= 32.5 and 74.0 <= lon <= 77.0:
            state_key = "punjab"
        elif 8.0 <= lat <= 13.5 and 76.0 <= lon <= 80.0:
            state_key = "tamil nadu"
        elif 20.0 <= lat <= 24.5 and 68.0 <= lon <= 74.0:
            state_key = "gujarat"

        info = self.groundwater_database[state_key]
        return {
            "latitude": lat,
            "longitude": lon,
            "region_inferred": state_key.title(),
            "average_depth_meters": info["average_depth_meters"],
            "trend": info["trend"],
            "water_quality": info["quality"],
            "recommended_drilling_depth_meters": info["recommended_depth_meters"]
        }

    async def predict_bore_well_depth(self, soil_type: str, rainfall_mm: int, region: str) -> Dict[str, Any]:
        """Predict optimal borewell drilling depth and strike probability based on geographic conditions."""
        self.logger.info(f"Predicting borewell depth for soil: {soil_type}, rainfall: {rainfall_mm}, region: {region}")
        region_clean = region.lower().strip()
        
        base_depth = 50.0
        # Retrieve average state depth
        for k, v in self.groundwater_database.items():
            if k in region_clean:
                base_depth = v["average_depth_meters"]
                break
                
        # Calculate strike success probability based on soil and rainfall
        soil_clean = soil_type.lower().strip()
        probability = 0.80
        
        if "sandy" in soil_clean:
            base_depth += 15.0
            probability -= 0.10
        elif "clay" in soil_clean:
            base_depth -= 5.0
            probability += 0.05
        elif "rock" in soil_clean:
            base_depth += 35.0
            probability -= 0.15
            
        if rainfall_mm < 400:
            base_depth += 25.0
            probability -= 0.20
        elif rainfall_mm > 1500:
            base_depth -= 10.0
            probability += 0.10
            
        return {
            "region": region.title(),
            "soil_type": soil_type,
            "predicted_bore_well_depth_meters": round(max(base_depth, 20.0), 1),
            "success_probability": round(max(min(probability, 0.95), 0.30), 2),
            "drill_recommendation": "Highly recommended" if probability >= 0.70 else "Caution: low success probability"
        }

    async def get_water_quality(self, source_type: str, state: str) -> Dict[str, Any]:
        """Assess standard water health parameters based on source type and state."""
        self.logger.info(f"Fetching water quality for source: {source_type}, state: {state}")
        state_clean = state.lower().strip()
        source_clean = source_type.lower().strip()
        
        # Base quality attributes
        ph = 7.2
        tds_ppm = 250
        fluoride_mg_l = 0.8
        contamination_detected = False
        
        if "borewell" in source_clean or "groundwater" in source_clean:
            tds_ppm = 450
            fluoride_mg_l = 1.2
            if "rajasthan" in state_clean:
                tds_ppm = 850
                fluoride_mg_l = 1.8  # elevated fluoride risk
                contamination_detected = True
        elif "pond" in source_clean or "river" in source_clean:
            ph = 7.8
            tds_ppm = 180
            contamination_detected = True  # high biological risk
            
        is_safe = (6.5 <= ph <= 8.5) and (tds_ppm <= 500) and (fluoride_mg_l <= 1.5) and not contamination_detected
        
        safety_measures = []
        if tds_ppm > 500:
            safety_measures.append("Use Reverse Osmosis (RO) filtration before drinking.")
        if fluoride_mg_l > 1.5:
            safety_measures.append("Incorporate alum treatment or Activated Alumina defluoridation filters.")
        if contamination_detected:
            safety_measures.append("Boil water thoroughly for at least 10 minutes or use chlorine disinfection.")
            
        return {
            "source_type": source_type.title(),
            "state": state.title(),
            "parameters": {
                "pH": ph,
                "TDS_ppm": tds_ppm,
                "fluoride_mg_l": fluoride_mg_l,
                "pathogens_present": contamination_detected
            },
            "safe_for_drinking": is_safe,
            "remediation_steps": safety_measures if safety_measures else ["No additional filtration required. Safe to drink."]
        }

    async def get_rainwater_harvesting_plan(self, rainfall_mm: int, area_sqft: int, region: str) -> Dict[str, Any]:
        """Compute structural volume requirements and costs for a domestic rainwater harvesting system."""
        self.logger.info(f"Generating harvesting plan for area: {area_sqft}sqft, rainfall: {rainfall_mm}mm")
        
        # 1 sqft of area receives 0.93 liters of water per 1 mm rainfall (accounting for 10% runoff loss)
        run_off_coefficient = 0.85  # Roof run off efficiency
        harvestable_liters = round(area_sqft * 0.092903 * rainfall_mm * run_off_coefficient)
        
        # Determine technique type based on geographic region
        region_clean = region.lower().strip()
        tech_key = "plains"
        if "arid" in region_clean or "desert" in region_clean or "rajasthan" in region_clean:
            tech_key = "semi_arid"
        elif "hill" in region_clean or "mountain" in region_clean:
            tech_key = "hilly"
            
        guide = self.rainwater_harvesting_guides[tech_key]
        
        # Calculate optimal storage tank size
        recommended_tank_capacity = min(harvestable_liters, guide["tank_capacity_liters"])
        
        return {
            "roof_area_sqft": area_sqft,
            "annual_rainfall_mm": rainfall_mm,
            "total_annual_run_off_liters": harvestable_liters,
            "recommended_system_type": tech_key.title(),
            "recommended_tank_capacity_liters": recommended_tank_capacity,
            "techniques": guide["techniques"],
            "estimated_cost_inr": guide["cost_range_inr"],
            "maintenance_guidelines": guide["maintenance"]
        }

    async def get_irrigation_schedule(self, crop: str, rainfall_mm: int, soil_type: str) -> Dict[str, Any]:
        """Calculate optimal watering durations and quantities based on crop species and soil structure."""
        self.logger.info(f"Calculating irrigation schedule for crop: {crop}, rainfall: {rainfall_mm}")
        crop_clean = crop.lower().strip()
        
        water_req_liters_per_day = 5.0  # fallback
        if "rice" in crop_clean:
            water_req_liters_per_day = 15.0
        elif "tomato" in crop_clean:
            water_req_liters_per_day = 8.0
        elif "wheat" in crop_clean:
            water_req_liters_per_day = 6.0
            
        soil_clean = soil_type.lower().strip()
        frequency_days = 3
        if "sandy" in soil_clean:
            frequency_days = 2  # Sandy soils dry faster
        elif "clay" in soil_clean:
            frequency_days = 5  # Clay retains moisture
            
        # Rainfall deduction
        if rainfall_mm > 50:
            # High rainfall: delay irrigation
            next_irrigation_days = frequency_days + 4
            status = "soil_moisture_satisfied_by_rainfall"
        elif rainfall_mm > 15:
            next_irrigation_days = frequency_days + 1
            status = "partial_supplementary_irrigation_needed"
        else:
            next_irrigation_days = 1
            status = "immediate_irrigation_required"
            
        return {
            "crop": crop.title(),
            "soil_type": soil_type,
            "status": status,
            "water_requirement_liters_per_plant_day": water_req_liters_per_day,
            "recommended_frequency": f"Once every {frequency_days} days under normal dry spells",
            "next_watering_in_days": next_irrigation_days,
            "watering_depth_mm": 10 if "rice" in crop_clean else 4
        }
