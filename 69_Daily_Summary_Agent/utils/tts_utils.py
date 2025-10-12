from gtts import gTTS
import os
from config import Config

def generate_audio(text, filename="summary.mp3", lang=Config.TTS_LANGUAGE):
    tts = gTTS(text=text, lang=lang, slow=False)
    filepath = os.path.join(Config.AUDIO_DIR, filename)
    tts.save(filepath)
    return f"/{filepath}"
