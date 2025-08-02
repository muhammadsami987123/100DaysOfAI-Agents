import openai
from typing import Dict, Optional
from config import Config
from weather_service import WeatherService
from tts_service import TTSService

class WeatherAgent:
    """AI-powered weather agent using OpenAI for enhanced interactions"""
    
    def __init__(self):
        try:
            # Initialize OpenAI client with error handling
            if not Config.OPENAI_API_KEY:
                raise ValueError("OpenAI API key not found in configuration")
            
            self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
            self.weather_service = WeatherService()
            self.tts_service = TTSService()
            print("✅ WeatherAgent initialized successfully")
        except Exception as e:
            print(f"Warning: Could not initialize OpenAI client: {e}")
            self.client = None
            self.weather_service = WeatherService()
            self.tts_service = TTSService()
            print("⚠️ WeatherAgent initialized without OpenAI (limited functionality)")
        
    async def get_weather_response(self, city: str, include_voice: bool = True) -> Dict:
        """
        Get AI-enhanced weather response for a city
        
        Args:
            city (str): City name to get weather for
            include_voice (bool): Whether to include voice output
            
        Returns:
            Dict: Complete weather response with AI enhancement
        """
        try:
            print(f"🔍 Getting weather for: {city}")
            
            # Get raw weather data
            weather_data, error = await self.weather_service.get_weather_data(city)
            
            if error:
                print(f"❌ Weather service error: {error}")
                return {
                    "success": False,
                    "error": error,
                    "ai_response": f"I'm sorry, I couldn't get the weather for {city}. {error}",
                    "weather_data": None,
                    "voice_text": None
                }
            
            print(f"✅ Weather data retrieved for {weather_data.get('city', 'Unknown')}")
            
            # Enhance with AI if available
            if self.client:
                print("🤖 Enhancing with AI...")
                ai_response = await self._enhance_with_ai(weather_data)
            else:
                print("⚠️ Using fallback response (no AI)")
                ai_response = self._create_fallback_response(weather_data)
            
            # Create voice output if requested
            voice_text = None
            if include_voice and self.tts_service.enabled:
                print("🔊 Creating voice output...")
                voice_text = self.tts_service.create_weather_speech(weather_data)
                # Start voice playback asynchronously
                asyncio.create_task(self.tts_service.speak_text(voice_text))
            
            response = {
                "success": True,
                "weather_data": weather_data,
                "ai_response": ai_response,
                "voice_text": voice_text,
                "error": None
            }
            
            print("✅ Weather response prepared successfully")
            return response
            
        except Exception as e:
            print(f"❌ Unexpected error in get_weather_response: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "ai_response": f"I encountered an error while getting the weather for {city}. Please try again.",
                "weather_data": None,
                "voice_text": None
            }
    
    async def _enhance_with_ai(self, weather_data: Dict) -> str:
        """
        Use OpenAI to create an enhanced, natural weather response
        
        Args:
            weather_data (Dict): Raw weather data
            
        Returns:
            str: AI-enhanced weather description
        """
        try:
            if not self.client:
                return self._create_fallback_response(weather_data)
            
            # Prepare context for AI
            current = weather_data.get('current', {})
            forecast = weather_data.get('forecast', {})
            city = weather_data.get('city', 'Unknown')
            country = weather_data.get('country', '')
            
            # Get weather description
            weather_desc = self.weather_service.get_weather_description(
                current.get('weather_code', 0)
            )
            
            # Create prompt for AI
            prompt = f"""
            You are a friendly and knowledgeable weather assistant. Based on the following weather data, 
            provide a natural, conversational weather report that's informative and engaging.
            
            Location: {city}, {country}
            Current Temperature: {current.get('temperature')}°C
            Feels Like: {current.get('feels_like')}°C
            Weather Condition: {weather_desc}
            Humidity: {current.get('humidity')}%
            Wind Speed: {current.get('wind_speed')} km/h
            Today's High: {forecast.get('today_max')}°C
            Today's Low: {forecast.get('today_min')}°C
            Precipitation Chance: {forecast.get('precipitation_chance')}%
            
            Please provide a friendly, conversational weather report that includes:
            1. A warm greeting
            2. Current conditions in natural language
            3. How it feels (temperature vs feels like)
            4. Any notable weather conditions
            5. Today's forecast
            6. A helpful tip or recommendation based on the weather
            
            Keep it conversational, friendly, and under 150 words.
            """
            
            # Get AI response
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a friendly weather assistant. Provide helpful, conversational weather reports."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            print(f"✅ AI response generated: {len(ai_response)} characters")
            return ai_response
            
        except Exception as e:
            # Fallback to basic response if AI fails
            print(f"❌ AI enhancement failed: {e}")
            return self._create_fallback_response(weather_data)
    
    def _create_fallback_response(self, weather_data: Dict) -> str:
        """Create a fallback response without AI enhancement"""
        try:
            current = weather_data.get('current', {})
            city = weather_data.get('city', 'Unknown')
            
            temp = current.get('temperature')
            weather_desc = self.weather_service.get_weather_description(
                current.get('weather_code', 0)
            )
            
            response = f"Here's the current weather in {city}: {temp}°C with {weather_desc.lower()}. Have a great day!"
            print(f"✅ Fallback response created: {len(response)} characters")
            return response
        except Exception as e:
            print(f"❌ Fallback response failed: {e}")
            return f"Here's the current weather in {weather_data.get('city', 'Unknown')}. Have a great day!"
    
    async def get_weather_tips(self, weather_data: Dict) -> str:
        """
        Get AI-generated weather tips and recommendations
        
        Args:
            weather_data (Dict): Weather data
            
        Returns:
            str: Weather tips and recommendations
        """
        try:
            if not self.client:
                return "Stay comfortable and enjoy your day!"
            
            current = weather_data.get('current', {})
            forecast = weather_data.get('forecast', {})
            
            prompt = f"""
            Based on this weather data, provide 2-3 helpful tips or recommendations:
            
            Temperature: {current.get('temperature')}°C
            Weather: {self.weather_service.get_weather_description(current.get('weather_code', 0))}
            Humidity: {current.get('humidity')}%
            Wind: {current.get('wind_speed')} km/h
            Precipitation Chance: {forecast.get('precipitation_chance')}%
            
            Provide practical advice like clothing suggestions, activity recommendations, or safety tips.
            Keep it concise and friendly.
            """
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful weather advisor providing practical tips."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            tips = response.choices[0].message.content.strip()
            print(f"✅ Weather tips generated: {len(tips)} characters")
            return tips
            
        except Exception as e:
            print(f"❌ Weather tips failed: {e}")
            return "Stay comfortable and enjoy your day!"
    
    def stop_voice(self):
        """Stop any ongoing voice output"""
        try:
            self.tts_service.stop_speaking()
            print("✅ Voice stopped")
        except Exception as e:
            print(f"❌ Error stopping voice: {e}")

# Import asyncio for async operations
import asyncio 