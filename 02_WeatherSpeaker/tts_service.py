import os
import tempfile
import asyncio
from typing import Optional
import pyttsx3
from gtts import gTTS
from config import Config

class TTSService:
    """Text-to-Speech service for weather announcements"""
    
    def __init__(self):
        self.enabled = Config.TTS_ENABLED
        self.language = Config.TTS_LANGUAGE
        self.voice_rate = Config.TTS_VOICE_RATE
        
        # Initialize pyttsx3 engine
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', self.voice_rate)
            self.engine.setProperty('volume', 0.9)
            
            # Try to set a good voice
            voices = self.engine.getProperty('voices')
            if voices:
                # Prefer female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                else:
                    # Use first available voice
                    self.engine.setProperty('voice', voices[0].id)
        except Exception as e:
            print(f"Warning: Could not initialize pyttsx3: {e}")
            self.engine = None
    
    async def speak_text(self, text: str) -> bool:
        """
        Convert text to speech and play it
        
        Args:
            text (str): Text to convert to speech
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.enabled or not text:
            return False
            
        try:
            # Use pyttsx3 for immediate playback
            if self.engine:
                # Run in a separate thread to avoid blocking
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self._speak_sync, text)
                return True
            else:
                # Fallback to gTTS
                return await self._speak_with_gtts(text)
                
        except Exception as e:
            print(f"TTS Error: {e}")
            return False
    
    def _speak_sync(self, text: str):
        """Synchronous speech function for pyttsx3"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"pyttsx3 error: {e}")
    
    async def _speak_with_gtts(self, text: str) -> bool:
        """Fallback TTS using gTTS"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_path = temp_file.name
            
            # Generate speech
            tts = gTTS(text=text, lang=self.language, slow=False)
            tts.save(temp_path)
            
            # Play the audio file
            if os.name == 'nt':  # Windows
                os.system(f'start {temp_path}')
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open {temp_path}' if os.uname().sysname == 'Darwin' else f'xdg-open {temp_path}')
            
            # Clean up after a delay
            await asyncio.sleep(2)
            try:
                os.unlink(temp_path)
            except:
                pass
                
            return True
            
        except Exception as e:
            print(f"gTTS error: {e}")
            return False
    
    def create_weather_speech(self, weather_data: dict) -> str:
        """
        Create natural language weather description for speech
        
        Args:
            weather_data (dict): Weather data from API
            
        Returns:
            str: Natural language weather description
        """
        if not weather_data or 'current' not in weather_data:
            return "Sorry, I couldn't get the weather information."
        
        current = weather_data['current']
        city = weather_data.get('city', 'Unknown location')
        country = weather_data.get('country', '')
        
        temp = current.get('temperature')
        feels_like = current.get('feels_like')
        humidity = current.get('humidity')
        weather_code = current.get('weather_code')
        
        # Get weather description
        from weather_service import WeatherService
        weather_service = WeatherService()
        weather_desc = weather_service.get_weather_description(weather_code)
        
        # Build natural language description
        speech_parts = []
        
        # Location
        location = f"{city}"
        if country:
            location += f", {country}"
        speech_parts.append(f"Here's the weather for {location}")
        
        # Temperature
        if temp is not None:
            temp_text = f"Currently {temp}°C"
            if feels_like is not None and abs(temp - feels_like) > 2:
                temp_text += f", but it feels like {feels_like}°C"
            speech_parts.append(temp_text)
        
        # Weather condition
        if weather_desc:
            speech_parts.append(f"with {weather_desc.lower()}")
        
        # Humidity
        if humidity is not None:
            speech_parts.append(f"Humidity is {humidity}%")
        
        # Wind
        wind_speed = current.get('wind_speed')
        if wind_speed is not None:
            if wind_speed < 10:
                wind_desc = "light breeze"
            elif wind_speed < 20:
                wind_desc = "moderate wind"
            else:
                wind_desc = "strong wind"
            speech_parts.append(f"Wind is {wind_desc} at {wind_speed} kilometers per hour")
        
        # Today's forecast
        forecast = weather_data.get('forecast', {})
        today_max = forecast.get('today_max')
        today_min = forecast.get('today_min')
        
        if today_max is not None and today_min is not None:
            speech_parts.append(f"Today's high will be {today_max}°C and low {today_min}°C")
        
        # Precipitation chance
        precip_chance = forecast.get('precipitation_chance')
        if precip_chance is not None and precip_chance > 30:
            speech_parts.append(f"There's a {precip_chance}% chance of precipitation today")
        
        return ". ".join(speech_parts) + "."
    
    def stop_speaking(self):
        """Stop any ongoing speech"""
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass 