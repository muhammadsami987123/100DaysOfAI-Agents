import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    TTS_LANGUAGE = os.getenv("TTS_LANGUAGE", "en")
    AUDIO_DIR = os.getenv("AUDIO_DIR", "static")
    MAX_NEWS_HEADLINES = int(os.getenv("MAX_NEWS_HEADLINES", "5"))
    DEFAULT_NEWS_PREFERENCE = os.getenv("DEFAULT_NEWS_PREFERENCE", "General")
