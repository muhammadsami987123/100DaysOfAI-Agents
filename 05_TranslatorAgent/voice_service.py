import speech_recognition as sr
import pyttsx3
import threading
import queue
import logging
import platform
import subprocess
import sys
import time
from typing import Optional, Dict, Any
from config import TranslatorConfig, VOICE_SETTINGS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceService:
    """Voice service for speech-to-text and text-to-speech"""
    
    def __init__(self):
        """Initialize voice service"""
        self.recognizer = sr.Recognizer()
        self.engine = None
        self.speaking = False
        self.audio_queue = queue.Queue()
        
        # Initialize text-to-speech engine
        self._init_tts_engine()
    
    def _init_tts_engine(self):
        """Initialize text-to-speech engine with better error handling"""
        try:
            # Try to initialize the TTS engine
            self.engine = pyttsx3.init()
            
            # Set default properties
            self.engine.setProperty('rate', TranslatorConfig.SPEECH_RATE)
            self.engine.setProperty('volume', TranslatorConfig.VOICE_VOLUME)
            
            # Get available voices
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to set a good default voice
                self.engine.setProperty('voice', voices[0].id)
                logger.info(f"TTS engine initialized with {len(voices)} voices")
            else:
                logger.warning("No voices found in TTS engine")
            
            # Test the engine
            self._test_tts_engine()
            
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {str(e)}")
            self.engine = None
            # Try alternative initialization methods
            self._try_alternative_tts()
    
    def _test_tts_engine(self):
        """Test if TTS engine is working"""
        try:
            if self.engine:
                # Get current properties
                rate = self.engine.getProperty('rate')
                volume = self.engine.getProperty('volume')
                voices = self.engine.getProperty('voices')
                
                logger.info(f"TTS Test - Rate: {rate}, Volume: {volume}, Voices: {len(voices) if voices else 0}")
                
                # Try a simple test
                self.engine.say("Test")
                self.engine.runAndWait()
                logger.info("TTS engine test successful")
                
        except Exception as e:
            logger.error(f"TTS engine test failed: {str(e)}")
            self.engine = None
    
    def _try_alternative_tts(self):
        """Try alternative TTS initialization methods"""
        try:
            # Try different driver options based on platform
            if platform.system() == "Windows":
                # Try Windows-specific drivers
                drivers = ['sapi5', 'nsss', 'espeak']
            elif platform.system() == "Darwin":  # macOS
                drivers = ['nsss', 'espeak']
            else:  # Linux
                drivers = ['espeak', 'nsss']
            
            for driver in drivers:
                try:
                    logger.info(f"Trying TTS driver: {driver}")
                    self.engine = pyttsx3.init(driver)
                    
                    # Set properties
                    self.engine.setProperty('rate', TranslatorConfig.SPEECH_RATE)
                    self.engine.setProperty('volume', TranslatorConfig.VOICE_VOLUME)
                    
                    # Test
                    self.engine.say("Test")
                    self.engine.runAndWait()
                    
                    logger.info(f"Successfully initialized TTS with driver: {driver}")
                    return
                    
                except Exception as e:
                    logger.warning(f"Failed to initialize TTS with driver {driver}: {str(e)}")
                    continue
            
            logger.error("All TTS drivers failed")
            
        except Exception as e:
            logger.error(f"Alternative TTS initialization failed: {str(e)}")
    
    def speak_text(self, text: str, language: str = "en") -> Dict[str, Any]:
        """
        Convert text to speech with improved error handling
        
        Args:
            text: Text to speak
            language: Language code for voice selection
        
        Returns:
            Dictionary with result status
        """
        if not self.engine:
            return {"success": False, "error": "TTS engine not available. Please check audio drivers and system settings."}
        
        if not text or text.strip() == "":
            return {"success": False, "error": "No text provided to speak."}
        
        try:
            # Stop any ongoing speech
            self.stop_speaking()
            
            # Configure voice for language
            self._configure_voice_for_language(language)
            
            # Log the speech attempt
            logger.info(f"Attempting to speak: '{text[:50]}...' in language: {language}")
            
            # Speak in a separate thread
            def speak_thread():
                try:
                    self.speaking = True
                    logger.info("Starting speech...")
                    
                    # Split long text into sentences for better handling
                    sentences = text.split('. ')
                    for sentence in sentences:
                        if sentence.strip():
                            self.engine.say(sentence.strip())
                    
                    self.engine.runAndWait()
                    logger.info("Speech completed successfully")
                    
                except Exception as e:
                    logger.error(f"Speech error in thread: {str(e)}")
                finally:
                    self.speaking = False
            
            thread = threading.Thread(target=speak_thread)
            thread.daemon = True
            thread.start()
            
            # Wait a moment to ensure speech starts
            time.sleep(0.1)
            
            return {
                "success": True,
                "text": text,
                "language": language,
                "speaking": True
            }
            
        except Exception as e:
            logger.error(f"Speech error: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to speak text: {str(e)}. Check audio settings and drivers.",
                "text": text
            }
    
    def listen_for_speech(self, language: str = "en", timeout: int = 5) -> Dict[str, Any]:
        """
        Listen for speech and convert to text with improved error handling
        
        Args:
            language: Expected language for better recognition
            timeout: Timeout in seconds
        
        Returns:
            Dictionary with transcribed text
        """
        try:
            with sr.Microphone() as source:
                logger.info("Listening for speech...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
                logger.info("Processing speech...")
                
                # Recognize speech
                text = self.recognizer.recognize_google(audio, language=language)
                
                return {
                    "success": True,
                    "text": text,
                    "language": language,
                    "confidence": 0.8  # Google's confidence
                }
                
        except sr.WaitTimeoutError:
            return {
                "success": False,
                "error": "No speech detected within timeout. Please try speaking again.",
                "language": language
            }
        except sr.UnknownValueError:
            return {
                "success": False,
                "error": "Could not understand speech. Please speak more clearly.",
                "language": language
            }
        except sr.RequestError as e:
            return {
                "success": False,
                "error": f"Speech recognition service error: {str(e)}. Check internet connection.",
                "language": language
            }
        except Exception as e:
            logger.error(f"Speech recognition error: {str(e)}")
            return {
                "success": False,
                "error": f"Microphone error: {str(e)}. Check microphone permissions and settings.",
                "language": language
            }
    
    def stop_speaking(self) -> Dict[str, Any]:
        """Stop ongoing speech"""
        try:
            if self.engine and self.speaking:
                self.engine.stop()
                self.speaking = False
                logger.info("Speech stopped")
                return {"success": True, "stopped": True}
            else:
                return {"success": True, "stopped": False, "message": "No speech in progress"}
                
        except Exception as e:
            logger.error(f"Error stopping speech: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def is_speaking(self) -> bool:
        """Check if currently speaking"""
        return self.speaking
    
    def get_available_voices(self) -> Dict[str, Any]:
        """Get available voices"""
        try:
            if not self.engine:
                return {"success": False, "error": "TTS engine not available"}
            
            voices = self.engine.getProperty('voices')
            voice_list = []
            
            for voice in voices:
                voice_list.append({
                    "id": voice.id,
                    "name": voice.name,
                    "languages": voice.languages,
                    "gender": voice.gender
                })
            
            return {
                "success": True,
                "voices": voice_list,
                "count": len(voice_list)
            }
            
        except Exception as e:
            logger.error(f"Error getting voices: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def set_voice_properties(self, rate: Optional[int] = None, volume: Optional[float] = None) -> Dict[str, Any]:
        """Set voice properties"""
        try:
            if not self.engine:
                return {"success": False, "error": "TTS engine not available"}
            
            if rate is not None:
                self.engine.setProperty('rate', rate)
            
            if volume is not None:
                self.engine.setProperty('volume', volume)
            
            return {"success": True, "rate": rate, "volume": volume}
            
        except Exception as e:
            logger.error(f"Error setting voice properties: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _configure_voice_for_language(self, language: str):
        """Configure voice settings for specific language"""
        try:
            if not self.engine:
                return
            
            # Get language-specific settings
            lang_settings = VOICE_SETTINGS.get(language, VOICE_SETTINGS.get("en", {}))
            
            # Set rate
            if "rate" in lang_settings:
                self.engine.setProperty('rate', lang_settings["rate"])
            
            # Try to set voice for language
            voices = self.engine.getProperty('voices')
            if voices and "voice" in lang_settings:
                # Find voice for language
                target_voice = lang_settings["voice"]
                for voice in voices:
                    if target_voice in voice.id.lower():
                        self.engine.setProperty('voice', voice.id)
                        logger.info(f"Set voice for language {language}: {voice.name}")
                        break
            
        except Exception as e:
            logger.error(f"Error configuring voice for language {language}: {str(e)}")
    
    def health_check(self) -> Dict[str, Any]:
        """Check voice service health with detailed diagnostics"""
        try:
            # Check TTS engine
            tts_available = self.engine is not None
            tts_details = "Available" if tts_available else "Not available"
            
            # Check microphone
            mic_available = False
            mic_details = "Not available"
            try:
                with sr.Microphone() as source:
                    mic_available = True
                    mic_details = "Available"
            except Exception as e:
                mic_details = f"Error: {str(e)}"
            
            # Test speech recognition
            sr_available = False
            sr_details = "Not available"
            try:
                # Quick test
                self.recognizer.recognize_google(sr.AudioData(b'', 16000, 2))
                sr_available = True
                sr_details = "Available"
            except Exception as e:
                sr_details = f"Error: {str(e)}"
            
            # Get system info
            system_info = {
                "platform": platform.system(),
                "python_version": sys.version,
                "speech_recognition_version": sr.__version__,
                "pyttsx3_available": "pyttsx3" in sys.modules
            }
            
            return {
                "status": "healthy" if (tts_available or mic_available) else "unhealthy",
                "tts_available": tts_available,
                "tts_details": tts_details,
                "microphone_available": mic_available,
                "microphone_details": mic_details,
                "speech_recognition_available": sr_available,
                "speech_recognition_details": sr_details,
                "speaking": self.speaking,
                "system_info": system_info
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "tts_available": False,
                "microphone_available": False,
                "speech_recognition_available": False,
                "speaking": False
            }
    
    def get_troubleshooting_tips(self) -> Dict[str, Any]:
        """Get troubleshooting tips for voice issues"""
        tips = {
            "windows": [
                "Check Windows Audio settings",
                "Ensure speakers/headphones are connected and working",
                "Try running as administrator",
                "Install Windows Media Player if not present",
                "Check microphone permissions in Windows Settings > Privacy > Microphone"
            ],
            "macos": [
                "Check System Preferences > Sound",
                "Ensure microphone permissions in System Preferences > Security & Privacy > Microphone",
                "Try using external speakers/headphones",
                "Check Audio MIDI Setup utility"
            ],
            "linux": [
                "Install espeak: sudo apt-get install espeak",
                "Check ALSA/PulseAudio configuration",
                "Try: sudo apt-get install python3-pyaudio",
                "Check microphone permissions",
                "Test with: speaker-test -t wav"
            ],
            "general": [
                "Restart the application",
                "Check system volume and mute settings",
                "Try different audio output devices",
                "Update audio drivers",
                "Test with a simple text first"
            ]
        }
        
        current_platform = platform.system().lower()
        platform_tips = tips.get(current_platform, [])
        
        return {
            "platform": current_platform,
            "platform_tips": platform_tips,
            "general_tips": tips["general"]
        } 