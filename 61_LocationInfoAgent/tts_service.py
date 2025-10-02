import os
import tempfile
import asyncio
import io
from typing import Optional

# Conditional imports for TTS engines
try:
    import pyttsx3
except ImportError:
    pyttsx3 = None
    print("Warning: pyttsx3 not installed. Local TTS will be unavailable.")

try:
    from gtts import gTTS
except ImportError:
    gTTS = None
    print("Warning: gTTS not installed. Google TTS fallback will be unavailable.")

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None
    print("Warning: OpenAI library not installed. OpenAI TTS will be unavailable.")

from config import Config

class TTSService:
    """Text-to-Speech service for location announcements"""
    
    def __init__(self):
        self.enabled = Config.TTS_ENABLED
        self.engine_type = Config.TTS_ENGINE
        self.language = Config.TTS_LANGUAGE
        self.voice_rate = Config.TTS_VOICE_RATE
        self.openai_api_key = Config.OPENAI_API_KEY
        self.max_chars = Config.MAX_TTS_CHARS

        self.openai_client = None
        if self.openai_api_key and OpenAI:
            self.openai_client = OpenAI(api_key=self.openai_api_key)

        self.pyttsx3_engine = None
        if pyttsx3:
            try:
                self.pyttsx3_engine = pyttsx3.init()
                self.pyttsx3_engine.setProperty('rate', self.voice_rate)
                self.pyttsx3_engine.setProperty('volume', 0.9)
                self._set_pyttsx3_voice()
            except Exception as e:
                print(f"Warning: Could not initialize pyttsx3: {e}")
                self.pyttsx3_engine = None
    
    def _set_pyttsx3_voice(self):
        """Try to set a good voice for pyttsx3"""
        if not self.pyttsx3_engine:
            return

        voices = self.pyttsx3_engine.getProperty('voices')
        if voices:
            # Prefer female voice if available, then male, then first available
            target_gender = "female"
            if Config.DEFAULT_VOICE_FEMALE in [v.name.lower() for v in voices]:
                for voice in voices:
                    if Config.DEFAULT_VOICE_FEMALE in voice.name.lower():
                        self.pyttsx3_engine.setProperty('voice', voice.id)
                        return
            
            target_gender = "male"
            if Config.DEFAULT_VOICE_MALE in [v.name.lower() for v in voices]:
                for voice in voices:
                    if Config.DEFAULT_VOICE_MALE in voice.name.lower():
                        self.pyttsx3_engine.setProperty('voice', voice.id)
                        return

            for voice in voices:
                if 'female' in voice.name.lower():
                    self.pyttsx3_engine.setProperty('voice', voice.id)
                    return
            for voice in voices:
                if 'male' in voice.name.lower():
                    self.pyttsx3_engine.setProperty('voice', voice.id)
                    return
            
            self.pyttsx3_engine.setProperty('voice', voices[0].id) # Fallback to first available
        
    async def speak_text(self, text: str, gender: str = "female") -> bool:
        """
        Convert text to speech and play it using the configured TTS engine.
        Prioritizes OpenAI, then pyttsx3, then gTTS.
        """
        if not self.enabled or not text.strip():
            return False

        text_to_speak = self._sanitize_text(text)

        if self.engine_type == "openai" and self.openai_client:
            print("🔊 Using OpenAI TTS...")
            return await self._speak_with_openai(text_to_speak, gender)
        elif self.pyttsx3_engine:
            print("🔊 Using pyttsx3 TTS...")
            return await self._speak_with_pyttsx3(text_to_speak)
        elif gTTS:
            print("🔊 Using gTTS TTS (fallback)...")
            return await self._speak_with_gtts(text_to_speak)
        else:
            print("❌ No TTS engine available or enabled.")
            return False

    def _sanitize_text(self, text: str) -> str:
        """Clean and truncate text for TTS"""
        text = text.strip()
        if not text:
            raise ValueError("Empty text provided for TTS.")
        if len(text) > self.max_chars:
            print(f"Warning: Text truncated from {len(text)} to {self.max_chars} characters for TTS.")
            text = text[:self.max_chars]
        return text

    async def _speak_with_pyttsx3(self, text: str) -> bool:
        """Synchronous speech function for pyttsx3, run in executor to avoid blocking"""
        if not self.pyttsx3_engine:
            return False
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.pyttsx3_engine.say, text)
            await loop.run_in_executor(None, self.pyttsx3_engine.runAndWait)
            return True
        except Exception as e:
            print(f"❌ pyttsx3 error: {e}")
            return False
    
    async def _speak_with_gtts(self, text: str) -> bool:
        """Fallback TTS using gTTS, saves to a temporary file and plays it"""
        if not gTTS:
            return False
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_path = temp_file.name
            
            tts = gTTS(text=text, lang=self.language, slow=False)
            tts.save(temp_path)
            
            if os.name == 'nt':  # Windows
                os.system(f'start {temp_path}')
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open {temp_path}' if os.uname().sysname == 'Darwin' else f'xdg-open {temp_path}')
            
            await asyncio.sleep(len(text) / (self.voice_rate / 60)) # Approximate duration
            try:
                os.unlink(temp_path)
            except Exception as e:
                print(f"Warning: Could not delete temporary gTTS file {temp_path}: {e}")
                pass
            return True
        except Exception as e:
            print(f"❌ gTTS error: {e}")
            return False

    async def _speak_with_openai(self, text: str, gender: str) -> bool:
        """OpenAI TTS integration"""
        if not self.openai_client:
            return False
        try:
            voice = Config.DEFAULT_VOICE_FEMALE if gender.lower() == "female" else Config.DEFAULT_VOICE_MALE
            model_candidates = ["tts-1", "tts-1-hd"]
            
            last_error: Optional[Exception] = None
            for model_name in model_candidates:
                try:
                    speech_response = await self.openai_client.audio.speech.create(
                        model=model_name,
                        voice=voice,
                        input=text,
                    )
                    
                    # Stream the audio response to a temporary file and play it
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                        temp_path = temp_file.name
                        speech_response.stream_to_file(temp_path)
                    
                    if os.name == 'nt':  # Windows
                        os.system(f'start {temp_path}')
                    elif os.name == 'posix':  # macOS and Linux
                        os.system(f'open {temp_path}' if os.uname().sysname == 'Darwin' else f'xdg-open {temp_path}')
                    
                    await asyncio.sleep(len(text) / (self.voice_rate / 60)) # Approximate duration
                    try:
                        os.unlink(temp_path)
                    except Exception as e:
                        print(f"Warning: Could not delete temporary OpenAI TTS file {temp_path}: {e}")
                        pass

                    return True
                except Exception as e:
                    print(f"❌ OpenAI TTS failed with model {model_name}: {e}")
                    last_error = e
                    continue
            
            print(f"❌ All OpenAI TTS models failed: {last_error}")
            return False # Fallback if all OpenAI models fail
        except Exception as e:
            print(f"❌ Unexpected OpenAI TTS error: {e}")
            return False
    
    def stop_speaking(self):
        """Stop any ongoing speech"""
        if self.pyttsx3_engine:
            try:
                self.pyttsx3_engine.stop()
                print("✅ pyttsx3 voice stopped")
            except Exception as e:
                print(f"❌ Error stopping pyttsx3 voice: {e}")
        # For gTTS and OpenAI, stopping means the temporary file finishes playing,
        # or the process that started it is terminated, which is harder to control
        # directly within this async function once os.system is called.
        # A more robust solution for external players would involve tracking PIDs.
        print("⚠️ Stop functionality for gTTS/OpenAI TTS is limited to the player process.")
