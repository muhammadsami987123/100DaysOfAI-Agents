import httpx
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any, Tuple
from config import Config

class LocationService:
    """Service class for fetching location data, map embeds, and images"""
    
    def __init__(self):
        self.google_maps_api_key = Config.GOOGLE_MAPS_API_KEY
        self.image_search_api_key = Config.IMAGE_SEARCH_API_KEY
        self.image_search_base_url = Config.IMAGE_SEARCH_BASE_URL
        self.http_client = httpx.AsyncClient()

    async def get_location_coordinates(self, location_name: str) -> Tuple[Optional[float], Optional[float]]:
        """Fetches latitude and longitude for a given location using a geocoding service."""
        try:
            # Using Open-Meteo's geocoding as an example, similar to WeatherSpeaker
            geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
            params = {
                "name": location_name,
                "count": 1,
                "language": "en",
                "format": "json"
            }
            response = await self.http_client.get(geocoding_url, params=params, timeout=10)
            response.raise_for_status()
            geocoding_data = response.json()

            if geocoding_data and geocoding_data.get("results"):
                location = geocoding_data["results"][0]
                return location["latitude"], location["longitude"]
            return None, None
        except httpx.RequestError as e:
            print(f"Network error fetching coordinates for {location_name}: {e}")
            return None, None
        except Exception as e:
            print(f"Error fetching coordinates for {location_name}: {e}")
            return None, None

    async def get_location_data(self, location_name: str) -> Dict[str, Any]:
        """Fetches comprehensive information about a location, prioritizing Wikipedia."""
        data = {
            "name": location_name,
            "summary": "",
            "facts": [],
            "culture": "",
            "language": "",
            "attractions": [],
            "wikipedia_url": None
        }
        try:
            wiki_url = f"https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": location_name,
                "srlimit": 1
            }
            response = await self.http_client.get(wiki_url, params=params, timeout=10)
            response.raise_for_status()
            search_results = response.json()

            if search_results.get("query") and search_results["query"].get("search"):
                page_title = search_results["query"]["search"][0]["title"]
                
                # Get summary and full URL
                params_summary = {
                    "action": "query",
                    "format": "json",
                    "prop": "extracts|info",
                    "exintro": True,
                    "explaintext": True,
                    "titles": page_title,
                    "inprop": "url"
                }
                response_summary = await self.http_client.get(wiki_url, params=params_summary, timeout=10)
                response_summary.raise_for_status()
                summary_data = response_summary.json()
                
                page_id = next(iter(summary_data["query"]["pages"]))
                page_content = summary_data["query"]["pages"][page_id]
                data["summary"] = page_content.get("extract", "No summary available.")
                data["wikipedia_url"] = page_content.get("fullurl")

                # For more structured data (facts, culture, language, attractions), 
                # we might need to do some light scraping or more advanced API calls. 
                # For now, we'll rely on the AI to process the summary and fill these.
                
            return data

        except httpx.RequestError as e:
            print(f"Network error fetching Wikipedia data for {location_name}: {e}")
        except Exception as e:
            print(f"Error fetching Wikipedia data for {location_name}: {e}")
        
        # Fallback if Wikipedia fails
        data["summary"] = f"Could not retrieve detailed information for {location_name} from Wikipedia. "
        return data

    def get_map_embed_url(self, latitude: float, longitude: float, zoom: int = 10) -> Optional[str]:
        """Generates a Google Maps embed URL for the given coordinates."""
        if not self.google_maps_api_key:
            return None
        
        # Example Google Maps Embed API URL
        # Note: This requires enabling the Maps Embed API in Google Cloud Console
        return f"https://www.google.com/maps/embed/v1/place?key={self.google_maps_api_key}&q={latitude},{longitude}&zoom={zoom}"

    async def get_images(self, location_name: str, count: int = 3) -> List[str]:
        """Fetches image URLs for the location (mocked for now, or using Unsplash/Wikimedia)."""
        if not self.image_search_api_key or not self.image_search_base_url:
            print("Warning: Image search API keys/URLs not configured. Using mocked images.")
            # Mocked images for demo purposes
            return [
                "https://via.placeholder.com/400x300?text=Location+Image+1",
                "https://via.placeholder.com/400x300?text=Location+Image+2",
                "https://via.placeholder.com/400x300?text=Location+Image+3"
            ]
        
        # Example: Unsplash API integration (requires registration and API key)
        # For a real implementation, you would replace this with actual API calls.
        try:
            unsplash_url = "https://api.unsplash.com/search/photos"
            headers = {"Authorization": f"Client-ID {self.image_search_api_key}"}
            params = {"query": location_name, "per_page": count}
            
            response = await self.http_client.get(unsplash_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            images_data = response.json()
            
            image_urls = []
            for result in images_data.get("results", [])[:count]:
                image_urls.append(result["urls"]["regular"])
            return image_urls

        except httpx.RequestError as e:
            print(f"Network error fetching images for {location_name}: {e}. Using mocked images.")
        except Exception as e:
            print(f"Error fetching images for {location_name}: {e}. Using mocked images.")
        
        # Fallback to mocked images if API fails or is not configured
        return [
            "https://via.placeholder.com/400x300?text=Location+Image+1",
            "https://via.placeholder.com/400x300?text=Location+Image+2",
            "https://via.placeholder.com/400x300?text=Location+Image+3"
        ]

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.http_client.aclose()
