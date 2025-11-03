import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    # Optional: OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MUSIC_DIR = "music" # Directory where music files are stored
    SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".ogg"]
