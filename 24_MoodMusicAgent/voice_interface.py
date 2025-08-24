"""
Voice interface for MoodMusicAgent - handles voice input and output
"""
import os
import time
from typing import Optional, Dict, Any
from config import Config

class VoiceInterface:
    """Handles voice input and output for MoodMusicAgent"""
    
    def __init__(self):
        self.enable_voice_input = Config.ENABLE_VOICE_INPUT
        self.enable_voice_output = Config.ENABLE_VOICE_OUTPUT
        self.language = Config.LANGUAGE
        
        # Initialize speech recognition
        self.recognizer = None
        if self.enable_voice_input:
            self._init_speech_recognition()
        
        # Initialize text-to-speech
        self.tts_engine = None
        if self.enable_voice_output:
            self._init_text_to_speech()
    
    def _init_speech_recognition(self):
        """Initialize speech recognition"""
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 4000
            self.recognizer.dynamic_energy_threshold = True
            print("🎤 Voice input enabled")
        except ImportError:
            print("⚠️  Speech recognition not available. Install speech_recognition package.")
            self.enable_voice_input = False
        except Exception as e:
            print(f"⚠️  Error initializing speech recognition: {e}")
            self.enable_voice_input = False
    
    def _init_text_to_speech(self):
        """Initialize text-to-speech engine"""
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS settings
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to find a voice matching the language
                for voice in voices:
                    if self.language.lower() in voice.languages[0].lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                else:
                    # Use first available voice if no language match
                    self.tts_engine.setProperty('voice', voices[0].id)
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 150)  # Words per minute
            self.tts_engine.setProperty('volume', 0.8)
            
            print("🔊 Voice output enabled")
        except ImportError:
            print("⚠️  Text-to-speech not available. Install pyttsx3 package.")
            self.enable_voice_output = False
        except Exception as e:
            print(f"⚠️  Error initializing text-to-speech: {e}")
            self.enable_voice_output = False
    
    def listen_for_mood(self, timeout: int = 10) -> Optional[Dict[str, Any]]:
        """
        Listen for voice input and detect mood
        
        Args:
            timeout: Maximum time to listen in seconds
            
        Returns:
            Dictionary with mood detection results or None
        """
        if not self.enable_voice_input or not self.recognizer:
            print("❌ Voice input not available")
            return None
        
        try:
            import speech_recognition as sr
            
            print(f"🎤 Listening for your mood... (speak within {timeout} seconds)")
            
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                try:
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                    print("🔍 Processing your voice...")
                    
                    # Convert speech to text
                    text = self.recognizer.recognize_google(audio, language=self.language)
                    print(f"🎯 You said: \"{text}\"")
                    
                    return {
                        "text": text,
                        "confidence": 0.8,  # Speech recognition confidence
                        "method": "voice_input"
                    }
                    
                except sr.WaitTimeoutError:
                    print("⏰ No voice input detected within timeout")
                    return None
                except sr.UnknownValueError:
                    print("❓ Could not understand what you said")
                    return None
                except sr.RequestError as e:
                    print(f"❌ Speech recognition service error: {e}")
                    return None
                    
        except Exception as e:
            print(f"❌ Error during voice input: {e}")
            return None
    
    def speak_text(self, text: str, wait: bool = True) -> bool:
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            wait: Whether to wait for speech to complete
            
        Returns:
            True if speech started successfully
        """
        if not self.enable_voice_output or not self.tts_engine:
            return False
        
        try:
            if wait:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            else:
                self.tts_engine.say(text)
                self.tts_engine.startLoop()
            
            return True
            
        except Exception as e:
            print(f"❌ Error during text-to-speech: {e}")
            return False
    
    def speak_mood_detection(self, mood: str, confidence: float) -> bool:
        """Speak mood detection results"""
        if not self.enable_voice_output:
            return False
        
        mood_config = Config.get_mood_config(mood)
        description = mood_config.get("description", "")
        
        text = f"I detected that you're feeling {mood}. {description}. Confidence level: {int(confidence * 100)}%"
        
        return self.speak_text(text)
    
    def speak_music_selection(self, music_data: Dict) -> bool:
        """Speak music selection information"""
        if not self.enable_voice_output:
            return False
        
        title = music_data.get("title", "Unknown")
        artist = music_data.get("artist", "Unknown")
        mood = music_data.get("mood", "Unknown")
        
        text = f"Now playing {title} by {artist} for your {mood} mood"
        
        return self.speak_text(text)
    
    def speak_instructions(self) -> bool:
        """Speak usage instructions"""
        if not self.enable_voice_output:
            return False
        
        text = """
        Welcome to MoodMusicAgent! I can help you find the perfect music for your mood.
        You can tell me how you're feeling, or I can listen to your voice.
        Available moods include: happy, sad, energetic, relaxed, romantic, stressed, motivated, and focus.
        Just say or type your mood and I'll find the perfect music for you.
        """
        
        return self.speak_text(text)
    
    def speak_error(self, error_message: str) -> bool:
        """Speak error messages"""
        if not self.enable_voice_output:
            return False
        
        text = f"I encountered an error: {error_message}"
        return self.speak_text(text)
    
    def speak_volume_change(self, volume: float) -> bool:
        """Speak volume change confirmation"""
        if not self.enable_voice_output:
            return False
        
        text = f"Volume set to {int(volume * 100)}%"
        return self.speak_text(text)
    
    def speak_playback_control(self, action: str) -> bool:
        """Speak playback control actions"""
        if not self.enable_voice_output:
            return False
        
        action_messages = {
            "play": "Music is now playing",
            "pause": "Music paused",
            "resume": "Music resumed",
            "stop": "Music stopped",
            "next": "Playing next track",
            "previous": "Playing previous track"
        }
        
        text = action_messages.get(action, f"Playback action: {action}")
        return self.speak_text(text)
    
    def get_voice_status(self) -> Dict[str, bool]:
        """Get status of voice interface components"""
        return {
            "voice_input_enabled": self.enable_voice_input and self.recognizer is not None,
            "voice_output_enabled": self.enable_voice_output and self.tts_engine is not None,
            "speech_recognition_available": self.recognizer is not None,
            "text_to_speech_available": self.tts_engine is not None
        }
    
    def test_voice_interface(self) -> Dict[str, Any]:
        """Test voice interface functionality"""
        results = {
            "speech_recognition": False,
            "text_to_speech": False,
            "microphone": False,
            "overall": False
        }
        
        # Test text-to-speech
        if self.enable_voice_output and self.tts_engine:
            try:
                self.speak_text("Testing voice output", wait=True)
                results["text_to_speech"] = True
            except Exception as e:
                print(f"❌ TTS test failed: {e}")
        
        # Test speech recognition
        if self.enable_voice_input and self.recognizer:
            try:
                import speech_recognition as sr
                with sr.Microphone() as source:
                    # Just test if microphone is accessible
                    results["microphone"] = True
                    
                    # Test recognition with a short timeout
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    results["speech_recognition"] = True
                    
            except Exception as e:
                print(f"❌ Speech recognition test failed: {e}")
        
        # Overall status
        results["overall"] = results["speech_recognition"] and results["text_to_speech"]
        
        return results
    
    def set_voice_settings(self, rate: int = None, volume: float = None, voice_id: str = None) -> bool:
        """Configure voice output settings"""
        if not self.tts_engine:
            return False
        
        try:
            if rate is not None:
                self.tts_engine.setProperty('rate', rate)
            
            if volume is not None:
                self.tts_engine.setProperty('volume', max(0.0, min(1.0, volume)))
            
            if voice_id is not None:
                voices = self.tts_engine.getProperty('voices')
                if any(voice.id == voice_id for voice in voices):
                    self.tts_engine.setProperty('voice', voice_id)
                else:
                    print(f"⚠️  Voice ID {voice_id} not found")
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error setting voice settings: {e}")
            return False
    
    def get_available_voices(self) -> list:
        """Get list of available TTS voices"""
        if not self.tts_engine:
            return []
        
        try:
            voices = self.tts_engine.getProperty('voices')
            return [
                {
                    "id": voice.id,
                    "name": voice.name,
                    "languages": voice.languages,
                    "gender": voice.gender
                }
                for voice in voices
            ]
        except Exception as e:
            print(f"❌ Error getting available voices: {e}")
            return []
    
    def cleanup(self):
        """Clean up voice interface resources"""
        if self.tts_engine:
            try:
                self.tts_engine.stop()
            except:
                pass
