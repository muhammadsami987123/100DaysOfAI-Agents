import os
import uuid
from gtts import gTTS
# import pyttsx3 # For offline fallback, if needed

from backend.config import Config

class TTSService:
    def __init__(self):
        os.makedirs(Config.AUDIO_DIR, exist_ok=True)

    def generate_audio(self, text: str, lang: str = "en") -> str:
        """Generates an MP3 audio file from the given text and returns its URL."""
        audio_filename = f"motivation_{uuid.uuid4().hex}.mp3"
        audio_path = os.path.join(Config.AUDIO_DIR, audio_filename)

        if Config.TTS_ENGINE == "gtts":
            try:
                tts = gTTS(text=text, lang=lang, slow=False)
                tts.save(audio_path)
            except Exception as e:
                print(f"Error with gTTS, falling back to pyttsx3 (if enabled): {e}")
                # Fallback logic could go here if pyttsx3 is integrated
                # For now, if gTTS fails, we'll raise the error or handle it.
                raise
        # elif Config.TTS_ENGINE == "pyttsx3":
        #     engine = pyttsx3.init()
        #     engine.save_to_file(text, audio_path)
        #     engine.runAndWait()
        else:
            raise ValueError(f"Unsupported TTS engine: {Config.TTS_ENGINE}")

        return f"/{Config.AUDIO_DIR}/{audio_filename}"

