"""
Voice handler for JarvisMouseControl
Handles speech recognition and text-to-speech functionality
"""

import speech_recognition as sr
import pyttsx3
import threading
import time
from typing import Optional, Callable, Dict, Any
from config import CONFIG

class VoiceHandler:
    """Handles voice input and output for JarvisMouseControl"""
    
    def __init__(self, language: str = "en"):
        """Initialize voice handler with specified language"""
        self.language = language
        self.recognizer = None
        self.tts_engine = None
        self.is_listening = False
        self.voice_callback = None
        self.listening_thread = None
        self.microphone_index = None
        
        # Initialize speech recognition
        self._init_speech_recognition()
        
        # Initialize text-to-speech
        self._init_tts()
    
    def _init_speech_recognition(self):
        """Initialize speech recognition"""
        try:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = CONFIG.VOICE_ENERGY_THRESHOLD
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = CONFIG.VOICE_PHRASE_TIMEOUT
            
            print("✅ Speech recognition initialized")
        except Exception as e:
            print(f"❌ Error initializing speech recognition: {e}")
            self.recognizer = None
    
    def _init_tts(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS settings
            self.tts_engine.setProperty('rate', CONFIG.TTS_RATE)
            self.tts_engine.setProperty('volume', CONFIG.TTS_VOLUME)
            
            # Try to set voice by ID
            voices = self.tts_engine.getProperty('voices')
            if voices and len(voices) > int(CONFIG.TTS_VOICE_ID):
                self.tts_engine.setProperty('voice', voices[int(CONFIG.TTS_VOICE_ID)].id)
            
            print("✅ Text-to-speech initialized")
        except Exception as e:
            print(f"❌ Error initializing TTS: {e}")
            self.tts_engine = None
    
    def start_listening(self, callback: Callable[[str], None], microphone_index: int = None):
        """
        Start continuous voice listening
        
        Args:
            callback: Function to call when voice command is recognized
            microphone_index: Index of microphone to use (None for default)
        """
        if not CONFIG.VOICE_ENABLED or not self.recognizer:
            print("🔇 Voice input is disabled or not available")
            return False
        
        # Find working microphone if not specified
        if microphone_index is None:
            working_mic = self._find_working_microphone()
            if working_mic is None:
                print("❌ No working microphone found for voice listening")
                return False
            microphone_index = working_mic
        
        self.voice_callback = callback
        self.is_listening = True
        self.microphone_index = microphone_index
        
        # Start listening in a separate thread
        self.listening_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listening_thread.start()
        
        print(f"🎤 Voice listening started (using microphone {microphone_index})")
        return True
    
    def stop_listening(self):
        """Stop voice listening"""
        self.is_listening = False
        if self.listening_thread:
            self.listening_thread.join(timeout=1.0)
        print("🔇 Voice listening stopped")
    
    def _listen_loop(self):
        """Main listening loop running in separate thread"""
        try:
            # Use the microphone index that was already found and passed
            if self.microphone_index is None:
                print("❌ No microphone index available for voice listening")
                self.is_listening = False
                return
            
            with sr.Microphone(device_index=self.microphone_index) as source:
                self._do_listening(source)
        except Exception as e:
            print(f"❌ Error in voice listening loop: {e}")
            print("💡 Voice input will be disabled")
            self.is_listening = False
    
    def _find_working_microphone(self):
        """Find a working microphone"""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            for i, mic_name in enumerate(mic_list):
                try:
                    # Skip output devices
                    if any(keyword in mic_name.lower() for keyword in ['output', 'speaker', 'playback']):
                        continue
                    
                    with sr.Microphone(device_index=i) as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                        print(f"✅ Found working microphone {i}: {mic_name}")
                        return i
                except Exception as e:
                    # Silently continue to next microphone
                    continue
            return None
        except Exception as e:
            print(f"❌ Error finding microphone: {e}")
            return None
    
    def _do_listening(self, source):
        """Perform the actual listening with the microphone source"""
        try:
            # Adjust for ambient noise
            print("🔧 Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("✅ Microphone ready for voice commands")
            
            while self.is_listening:
                try:
                    # Listen for audio with shorter timeout
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=3)
                    
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio, language=self._get_google_language_code())
                    
                    if text and self.voice_callback:
                        print(f"🎤 Heard: {text}")
                        self.voice_callback(text)
                        
                except sr.WaitTimeoutError:
                    # Timeout is normal, continue listening
                    continue
                except sr.UnknownValueError:
                    # Could not understand audio - don't print every time
                    continue
                except sr.RequestError as e:
                    print(f"❌ Speech recognition error: {e}")
                    time.sleep(2)  # Wait before retrying
                    continue
                except Exception as e:
                    print(f"❌ Unexpected error in voice recognition: {e}")
                    time.sleep(2)
                    continue
        except Exception as e:
            print(f"❌ Error in listening process: {e}")
            self.is_listening = False
    
    def _get_google_language_code(self) -> str:
        """Get Google Speech Recognition language code"""
        language_codes = {
            "en": "en-US",
            "ur": "ur-PK", 
            "hi": "hi-IN"
        }
        return language_codes.get(self.language, "en-US")
    
    def speak(self, text: str, blocking: bool = False):
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            blocking: Whether to block until speech is complete
        """
        if not CONFIG.TTS_ENABLED or not self.tts_engine:
            print(f"🔇 TTS disabled, would say: {text}")
            return
        
        try:
            if blocking:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            else:
                # Create a new TTS engine instance for threading to avoid "run loop already started" error
                def speak_thread():
                    try:
                        # Create completely new engine instance
                        engine = pyttsx3.init()
                        engine.setProperty('rate', CONFIG.TTS_RATE)
                        engine.setProperty('volume', CONFIG.TTS_VOLUME)
                        
                        # Set voice if available
                        voices = engine.getProperty('voices')
                        if voices and len(voices) > int(CONFIG.TTS_VOICE_ID):
                            engine.setProperty('voice', voices[int(CONFIG.TTS_VOICE_ID)].id)
                        
                        engine.say(text)
                        engine.runAndWait()
                    except Exception as e:
                        print(f"❌ TTS thread error: {e}")
                
                # Start thread and don't wait for it
                thread = threading.Thread(target=speak_thread, daemon=True)
                thread.start()
                # Give the thread a moment to start
                time.sleep(0.1)
            
            print(f"🔊 Speaking: {text}")
        except Exception as e:
            print(f"❌ Error speaking: {e}")
    
    def listen_once(self, timeout: float = 5.0) -> Optional[str]:
        """
        Listen for a single voice command
        
        Args:
            timeout: Maximum time to wait for speech
            
        Returns:
            Recognized text or None if no speech detected
        """
        if not CONFIG.VOICE_ENABLED or not self.recognizer:
            print("🔇 Voice input is disabled or not available")
            return None
        
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio, language=self._get_google_language_code())
                print(f"🎤 Heard: {text}")
                return text
        except sr.WaitTimeoutError:
            print("⏰ Listening timeout")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error in voice recognition: {e}")
            return None
    
    def set_language(self, language: str):
        """Change the voice handler language"""
        if language in CONFIG.SUPPORTED_LANGUAGES:
            self.language = language
            print(f"🌍 Voice language changed to: {CONFIG.LANGUAGE_NAMES.get(language, language)}")
            return True
        return False
    
    def set_tts_rate(self, rate: int):
        """Set TTS speech rate"""
        if self.tts_engine:
            self.tts_engine.setProperty('rate', rate)
            CONFIG.TTS_RATE = rate
            print(f"⚡ TTS rate set to: {rate}")
    
    def set_tts_volume(self, volume: float):
        """Set TTS volume (0.0 to 1.0)"""
        if self.tts_engine:
            self.tts_engine.setProperty('volume', max(0.0, min(1.0, volume)))
            CONFIG.TTS_VOLUME = volume
            print(f"🔊 TTS volume set to: {volume}")
    
    def get_available_voices(self) -> list:
        """Get list of available TTS voices"""
        if not self.tts_engine:
            return []
        
        try:
            voices = self.tts_engine.getProperty('voices')
            return [{"id": i, "name": voice.name, "languages": voice.languages} for i, voice in enumerate(voices)]
        except Exception as e:
            print(f"❌ Error getting voices: {e}")
            return []
    
    def set_voice(self, voice_id: int):
        """Set TTS voice by ID"""
        if not self.tts_engine:
            return False
        
        try:
            voices = self.tts_engine.getProperty('voices')
            if voices and 0 <= voice_id < len(voices):
                self.tts_engine.setProperty('voice', voices[voice_id].id)
                CONFIG.TTS_VOICE_ID = str(voice_id)
                print(f"🎤 Voice set to: {voices[voice_id].name}")
                return True
            else:
                print(f"❌ Invalid voice ID: {voice_id}")
                return False
        except Exception as e:
            print(f"❌ Error setting voice: {e}")
            return False
    
    def is_voice_available(self) -> bool:
        """Check if voice input is available"""
        return CONFIG.VOICE_ENABLED and self.recognizer is not None
    
    def is_tts_available(self) -> bool:
        """Check if text-to-speech is available"""
        return CONFIG.TTS_ENABLED and self.tts_engine is not None
    
    def test_microphone(self) -> bool:
        """Test if microphone is working"""
        try:
            # Try to get microphone list first
            mic_list = sr.Microphone.list_microphone_names()
            if not mic_list:
                print("⚠️  No microphones detected")
                return False
            
            print(f"🎤 Found {len(mic_list)} microphone(s)")
            
            # Use the same logic as _find_working_microphone
            working_mic = self._find_working_microphone()
            
            if working_mic is not None:
                print(f"✅ Microphone {working_mic} is working!")
                print("✅ Microphone test successful")
                return True
            else:
                print("❌ No working microphones found")
                print("💡 This is likely a Windows permission issue.")
                print("💡 Try running as administrator or check microphone permissions.")
                return False
                
        except Exception as e:
            print(f"❌ Microphone test failed: {e}")
            print("💡 This might be a permission issue. Try running as administrator.")
            return False
    
    def test_speakers(self) -> bool:
        """Test if speakers are working"""
        try:
            if self.tts_engine:
                self.speak("Speaker test", blocking=True)
                print("🔊 Speaker test successful")
                return True
            else:
                print("❌ TTS engine not available")
                return False
        except Exception as e:
            print(f"❌ Speaker test failed: {e}")
            return False
    
    def list_microphones(self) -> list:
        """List all available microphones"""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            return [{"id": i, "name": name} for i, name in enumerate(mic_list)]
        except Exception as e:
            print(f"❌ Error listing microphones: {e}")
            return []
    
    def select_microphone(self) -> Optional[int]:
        """Interactive microphone selection"""
        mics = self.list_microphones()
        if not mics:
            print("❌ No microphones found")
            return None
        
        print("🎤 Available microphones:")
        for mic in mics:
            print(f"  {mic['id']}: {mic['name']}")
        
        try:
            choice = input("Enter microphone number (or press Enter for default): ").strip()
            if not choice:
                return None
            
            mic_id = int(choice)
            if 0 <= mic_id < len(mics):
                print(f"✅ Selected microphone: {mics[mic_id]['name']}")
                return mic_id
            else:
                print("❌ Invalid microphone number")
                return None
        except ValueError:
            print("❌ Invalid input")
            return None