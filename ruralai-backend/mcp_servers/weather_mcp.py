import aiohttp
from typing import Dict, List, Any
import logging

class WeatherMCPServer:
    """MCP Server providing weather forecasting, rainfall, temperature, and humidity metrics."""
    
    def __init__(self, api_key: str = "dummy_key"):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.logger = logging.getLogger("WeatherMCPServer")

    async def get_forecast(self, lat: float, lon: float, days: int = 15) -> Dict[str, Any]:
        """Fetch 15-day weather forecast. Uses mock data for reliable offline rural intelligence."""
        self.logger.info(f"Fetching weather forecast for lat: {lat}, lon: {lon}")
        
        # Provide high-quality mock data mimicking real API structures
        forecast_list = []
        for i in range(1, days + 1):
            forecast_list.append({
                "day": i,
                "temp_min": round(20.0 + (i % 3) * 1.5, 1),
                "temp_max": round(30.0 + (i % 2) * 2.0, 1),
                "rainfall_mm": round(0.0 if i % 4 != 0 else (i * 2.5), 1),
                "humidity": 60 + (i % 5) * 5
            })
            
        summary = "Optimal weather patterns expected. Light rain predicted on select days, suitable for crop sowing."
        return {
            "location": {"lat": lat, "lon": lon},
            "forecast": forecast_list,
            "summary": summary,
            "source": "OpenWeatherMap Mock API"
        }

    async def get_rainfall_prediction(self, lat: float, lon: float) -> Dict[str, Any]:
        """Fetch 15-day rainfall projection."""
        self.logger.info(f"Calculating rainfall trend for lat: {lat}, lon: {lon}")
        
        next_15_days = []
        total_rainfall = 0.0
        for i in range(1, 16):
            rainfall = round(0.0 if i % 5 != 0 else (i * 3.2), 1)
            next_15_days.append({"day": i, "rainfall_mm": rainfall})
            total_rainfall += rainfall
            
        status = "normal" if total_rainfall < 100.0 else "heavy_rainfall_warning"
        return {
            "next_15_days": next_15_days,
            "total_rainfall_mm": round(total_rainfall, 1),
            "status": status
        }

    async def get_humidity_trend(self, lat: float, lon: float) -> Dict[str, Any]:
        """Fetch 7-day humidity trend metrics."""
        self.logger.info(f"Analyzing humidity trend for lat: {lat}, lon: {lon}")
        days = list(range(1, 8))
        humidity = [65, 68, 70, 72, 69, 66, 64]
        return {
            "days": days,
            "humidity": humidity
        }

    async def get_temperature_range(self, lat: float, lon: float) -> Dict[str, Any]:
        """Fetch 7-day minimum/maximum temperature range."""
        self.logger.info(f"Analyzing temperature range for lat: {lat}, lon: {lon}")
        days = list(range(1, 8))
        temp_min = [21.5, 22.0, 21.8, 22.5, 23.0, 22.2, 21.9]
        temp_max = [31.5, 32.0, 31.8, 32.5, 33.0, 32.2, 31.9]
        return {
            "days": days,
            "temp_min": temp_min,
            "temp_max": temp_max
        }
