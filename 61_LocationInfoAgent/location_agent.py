import openai
from typing import Dict, Optional, Any, Tuple
from config import Config
from location_service import LocationService
from tts_service import TTSService
import asyncio

class LocationInfoAgent:
    """AI-powered location information agent using OpenAI for enhanced interactions"""
    
    def __init__(self):
        self.client = None
        try:
            if Config.OPENAI_API_KEY:
                self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
            else:
                print("⚠️ Warning: OpenAI API key not found. AI features will be limited.")
            
            self.location_service = LocationService()
            self.tts_service = TTSService()
            print("✅ LocationInfoAgent initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing LocationInfoAgent: {e}")
            self.client = None # Ensure client is None if init fails
            self.location_service = LocationService()
            self.tts_service = TTSService()
            print("⚠️ LocationInfoAgent initialized with limited functionality")
        
    async def get_location_info(self, place: str, include_voice: bool = True) -> Dict[str, Any]:
        """
        Get AI-enhanced location information for a given place.
        
        Args:
            place (str): Name of the city, country, landmark, or region.
            include_voice (bool): Whether to include voice output.
            
        Returns:
            Dict: Complete location information with AI enhancement.
        """
        print(f"🔍 Getting info for: {place}")
        try:
            # Fetch coordinates
            latitude, longitude = await self.location_service.get_location_coordinates(place)
            if latitude is None or longitude is None:
                error_msg = f"Could not find coordinates for '{place}'. Please check the spelling."
                print(f"❌ {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "ai_response": f"I'm sorry, I couldn't find '{place}'. Please try another location.",
                    "location_data": {"name": place},
                    "map_embed_url": None,
                    "image_urls": [],
                    "voice_text": None
                }

            # Fetch raw location data (e.g., from Wikipedia)
            raw_location_data = await self.location_service.get_location_data(place)
            raw_location_data["latitude"] = latitude
            raw_location_data["longitude"] = longitude
            print(f"✅ Raw location data retrieved for {place}")

            # Fetch map embed URL
            map_embed_url = self.location_service.get_map_embed_url(latitude, longitude)
            if not map_embed_url:
                print("⚠️ Google Maps API key not configured or map embedding failed.")

            # Fetch images
            image_urls = await self.location_service.get_images(place)
            if not image_urls:
                print("⚠️ Image search API key not configured or image fetching failed.")
            
            # Enhance with AI if available
            if self.client:
                print("🤖 Enhancing with AI...")
                ai_response, voice_text_content = await self._enhance_with_ai(raw_location_data)
            else:
                print("⚠️ Using fallback response (no AI)")
                ai_response = self._create_fallback_response(raw_location_data)
                voice_text_content = ai_response # Fallback for voice also

            # Create voice output if requested and TTS is enabled
            spoken_output = None
            if include_voice and self.tts_service.enabled:
                print("🔊 Creating voice output...")
                # Use the AI-generated voice_text_content for speaking
                asyncio.create_task(self.tts_service.speak_text(voice_text_content))
                spoken_output = voice_text_content
            
            response = {
                "success": True,
                "location_data": raw_location_data,
                "ai_response": ai_response,
                "map_embed_url": map_embed_url,
                "image_urls": image_urls,
                "voice_text": spoken_output,
                "error": None
            }
            
            print("✅ Location response prepared successfully")
            return response
            
        except Exception as e:
            print(f"❌ Unexpected error in get_location_info: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "ai_response": f"I encountered an error while getting information for {place}. Please try again.",
                "location_data": {"name": place},
                "map_embed_url": None,
                "image_urls": [],
                "voice_text": None
            }
    
    async def _enhance_with_ai(self, location_data: Dict[str, Any]) -> Tuple[str, str]:
        """
        Use OpenAI to create an enhanced, natural language location report.
        Returns both a visual (text) and a potentially condensed voice-friendly (text) response.
        """
        if not self.client:
            fallback_response = self._create_fallback_response(location_data)
            return fallback_response, fallback_response

        prompt_template = """
        You are LocationInfoAgent, a voice-enabled AI assistant providing information about places. 
        Based on the following data, generate a comprehensive, natural, and conversational report. 
        The report should be suitable for both visual display and spoken delivery. 

        Include:
        1. A warm greeting and introduction to the place.
        2. Current facts or a concise overview.
        3. Insights into its culture and language.
        4. Key attractions or notable features.
        5. A short summary (aim for 90-120 seconds if spoken).
        
        Format the response clearly with headings for easy reading. The summary should ideally be at the end.
        
        Location Data:
        Name: {name}
        Summary: {summary}
        Wikipedia URL: {wikipedia_url}
        Latitude: {latitude}
        Longitude: {longitude}
        
        Your detailed response, using Markdown headings (## Overview, ## Culture, ## Language, ## Key Attractions) and bullet points for readability:
        """
        
        # Prepare context for AI
        name = location_data.get('name', 'Unknown Place')
        summary = location_data.get('summary', 'No detailed summary available.')
        wikipedia_url = location_data.get('wikipedia_url', 'Not available')
        latitude = location_data.get('latitude', 'N/A')
        longitude = location_data.get('longitude', 'N/A')

        # Construct the prompt
        prompt = prompt_template.format(
            name=name,
            summary=summary,
            wikipedia_url=wikipedia_url,
            latitude=latitude,
            longitude=longitude
        )

        try:
            response = await self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a friendly and knowledgeable AI assistant providing engaging location information. Focus on current facts, culture, language, and key attractions. Summarize effectively for voice output."}, # Custom system message
                    {"role": "user", "content": prompt}
                ],
                max_tokens=Config.MAX_TTS_CHARS, # Limit tokens to manage response length for TTS
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            print(f"✅ AI response generated: {len(ai_response)} characters")

            # Create a potentially shorter, more direct version for voice output
            voice_text_content = await self._create_voice_friendly_summary(ai_response, name)

            return ai_response, voice_text_content
            
        except Exception as e:
            print(f"❌ AI enhancement failed: {e}")
            fallback_response = self._create_fallback_response(location_data)
            return fallback_response, fallback_response

    async def _create_voice_friendly_summary(self, long_text: str, place_name: str) -> str:
        """
        Uses AI to create a concise, voice-friendly summary from a longer text.
        Ensures it's within the 90-120 second spoken length (approx 180-240 words for 120 secs at 120 wpm).
        """
        if not self.client:
            return f"Here is some information about {place_name}. " + long_text.split('.')[0] + "."

        try:
            # Estimate target word count for 90-120 seconds at 120-150 words per minute
            # 90 seconds * 120 wpm = 180 words
            # 120 seconds * 120 wpm = 240 words
            # Let's aim for a maximum of around 250 words for safety.
            target_words = 250
            target_chars = target_words * 5 # Average 5 characters per word
            
            prompt = f"""
            Condense the following text into a concise, voice-friendly summary about {place_name}. 
            It should be informative and engaging, focusing on key facts, culture, language, and attractions. 
            Keep it under {target_words} words (approximately {target_chars} characters) for spoken delivery within 90-120 seconds.
            
            Text to summarize:
            {long_text}
            """
            
            response = await self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specialized in summarizing location information for voice output. Prioritize clarity and conciseness."}, # Custom system message
                    {"role": "user", "content": prompt}
                ],
                max_tokens=Config.MAX_TTS_CHARS, 
                temperature=0.5 # Lower temperature for more factual summary
            )
            
            summary = response.choices[0].message.content.strip()
            print(f"✅ Voice-friendly summary generated: {len(summary)} characters")
            return summary

        except Exception as e:
            print(f"❌ Failed to generate voice-friendly summary: {e}. Using first part of detailed response.")
            return f"Here is some information about {place_name}. " + long_text.split('.')[0] + "." # Fallback

    def _create_fallback_response(self, location_data: Dict[str, Any]) -> str:
        """Create a fallback response without AI enhancement"""
        name = location_data.get('name', 'Unknown Place')
        summary = location_data.get('summary', 'No detailed summary available.')
        
        response = f"Here's some basic information about {name}: {summary}. Enjoy exploring!"
        print(f"✅ Fallback response created: {len(response)} characters")
        return response
    
    def stop_voice(self):
        """Stop any ongoing voice output"""
        try:
            self.tts_service.stop_speaking()
            print("✅ Voice stopped")
        except Exception as e:
            print(f"❌ Error stopping voice: {e}")
