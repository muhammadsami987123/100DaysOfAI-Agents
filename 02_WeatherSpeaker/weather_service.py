import requests
import json
from typing import Dict, Optional, Tuple
from config import Config

class WeatherService:
    """Service class for fetching weather data from Open-Meteo API"""
    
    def __init__(self):
        self.base_url = Config.WEATHER_API_BASE_URL
        
    async def get_weather_data(self, city: str) -> Tuple[Dict, Optional[str]]:
        """
        Fetch weather data for a given city
        
        Args:
            city (str): City name to get weather for
            
        Returns:
            Tuple[Dict, Optional[str]]: Weather data and error message if any
        """
        try:
            # First, get coordinates for the city
            geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search"
            params = {
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            }
            
            response = requests.get(geocoding_url, params=params, timeout=10)
            response.raise_for_status()
            
            geocoding_data = response.json()
            
            if not geocoding_data.get("results"):
                return {}, f"City '{city}' not found. Please check the spelling and try again."
            
            location = geocoding_data["results"][0]
            latitude = location["latitude"]
            longitude = location["longitude"]
            city_name = location["name"]
            country = location.get("country", "")
            
            # Get weather data using coordinates
            weather_url = f"{self.base_url}/forecast"
            weather_params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m",
                "hourly": "temperature_2m,weather_code",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
                "timezone": "auto"
            }
            
            weather_response = requests.get(weather_url, params=weather_params, timeout=10)
            weather_response.raise_for_status()
            
            weather_data = weather_response.json()
            
            # Process and format the weather data
            current = weather_data.get("current", {})
            daily = weather_data.get("daily", {})
            
            weather_info = {
                "city": city_name,
                "country": country,
                "coordinates": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "current": {
                    "temperature": current.get("temperature_2m"),
                    "feels_like": current.get("apparent_temperature"),
                    "humidity": current.get("relative_humidity_2m"),
                    "precipitation": current.get("precipitation"),
                    "weather_code": current.get("weather_code"),
                    "wind_speed": current.get("wind_speed_10m"),
                    "wind_direction": current.get("wind_direction_10m"),
                    "time": current.get("time")
                },
                "forecast": {
                    "today_max": daily.get("temperature_2m_max", [None])[0] if daily.get("temperature_2m_max") else None,
                    "today_min": daily.get("temperature_2m_min", [None])[0] if daily.get("temperature_2m_min") else None,
                    "precipitation_chance": daily.get("precipitation_probability_max", [None])[0] if daily.get("precipitation_probability_max") else None
                }
            }
            
            return weather_info, None
            
        except requests.exceptions.RequestException as e:
            return {}, f"Network error: Unable to fetch weather data. Please try again later."
        except Exception as e:
            return {}, f"Unexpected error: {str(e)}"
    
    def get_weather_description(self, weather_code: int) -> str:
        """Convert weather code to human-readable description"""
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            56: "Light freezing drizzle",
            57: "Dense freezing drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Light freezing rain",
            67: "Heavy freezing rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        
        return weather_codes.get(weather_code, "Unknown weather condition")
    
    def get_weather_icon(self, weather_code: int) -> str:
        """Get appropriate weather icon based on weather code"""
        if weather_code in [0, 1]:
            return "☀️"
        elif weather_code in [2, 3]:
            return "☁️"
        elif weather_code in [45, 48]:
            return "🌫️"
        elif weather_code in [51, 53, 55, 56, 57]:
            return "🌦️"
        elif weather_code in [61, 63, 65, 66, 67, 80, 81, 82]:
            return "🌧️"
        elif weather_code in [71, 73, 75, 77, 85, 86]:
            return "❄️"
        elif weather_code in [95, 96, 99]:
            return "⛈️"
        else:
            return "🌤️" 