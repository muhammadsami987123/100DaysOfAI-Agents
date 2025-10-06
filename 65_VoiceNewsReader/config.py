import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration for VoiceNewsReader"""

    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    # App
    APP_TITLE = "VoiceNewsReader"
    APP_DESCRIPTION = "AI agent that fetches trending news and reads it via TTS"

    # APIs
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
    BING_NEWS_KEY = os.getenv("BING_NEWS_KEY")

    # Gemini (preferred TTS)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_TTS_MODEL = os.getenv("GEMINI_TTS_MODEL", "gemspeak")

    # TTS fallbacks
    TTS_ENGINE = os.getenv("TTS_ENGINE", "gemini").lower()  # gemini|gtts|pyttsx3
    TTS_LANGUAGE = os.getenv("TTS_LANGUAGE", "en")
    TTS_DEFAULT_GENDER = os.getenv("TTS_DEFAULT_GENDER", "female")
    TTS_RATE = int(os.getenv("TTS_RATE", "150"))
    TTS_PITCH = float(os.getenv("TTS_PITCH", "1.0"))  # semantic for engines that support
    MAX_TTS_CHARS = int(os.getenv("MAX_TTS_CHARS", "8000"))

    # News defaults
    DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "us")
    DEFAULT_CATEGORY = os.getenv("DEFAULT_CATEGORY", "general")
    DEFAULT_LIMIT = int(os.getenv("DEFAULT_LIMIT", "5"))

    # Storage
    AUDIO_DIR = os.getenv("AUDIO_DIR", "audio")

    @classmethod
    def validate(cls):
        if not (cls.NEWSAPI_KEY or cls.BING_NEWS_KEY):
            print("⚠️ Warning: No news API key set. Set NEWSAPI_KEY or BING_NEWS_KEY in .env")
        if cls.TTS_ENGINE == "gemini" and not cls.GEMINI_API_KEY:
            print("⚠️ Warning: GEMINI_API_KEY not set. Falling back to gTTS/pyttsx3 if available.")
        return True


