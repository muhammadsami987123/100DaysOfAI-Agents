import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for LocationInfoAgent"""
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o-mini"
    
    # Location API Configuration (example, will need to be replaced with a real API)
    LOCATION_API_BASE_URL = "https://api.example.com/location" 
    
    # Google Maps API Key for embedding maps
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

    # Image Search API Key (example)
    IMAGE_SEARCH_API_KEY = os.getenv("IMAGE_SEARCH_API_KEY")
    IMAGE_SEARCH_BASE_URL = "https://api.unsplash.com"

    # TTS Configuration
    TTS_ENABLED = os.getenv("TTS_ENABLED", "True").lower() == "true"
    TTS_ENGINE = os.getenv("TTS_ENGINE", "openai").lower() # openai or gtts
    TTS_LANGUAGE = os.getenv("TTS_LANGUAGE", "en")
    TTS_VOICE_RATE = int(os.getenv("TTS_VOICE_RATE", "150"))
    DEFAULT_VOICE_FEMALE = "alloy"  # OpenAI TTS voice
    DEFAULT_VOICE_MALE = "echo"      # OpenAI TTS voice
    MAX_TTS_CHARS = 4096 # Max characters for TTS API to avoid overly long responses

    # Server Configuration
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # UI Configuration
    APP_TITLE = "LocationInfoAgent"
    APP_DESCRIPTION = "AI-powered location information assistant with voice capabilities"
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            # We can run without OpenAI, but it will be limited
            print("⚠️ Warning: OPENAI_API_KEY not found. AI features will be limited.")
        
        # We can run without maps or images, but it will be limited
        if not cls.GOOGLE_MAPS_API_KEY:
            print("⚠️ Warning: GOOGLE_MAPS_API_KEY not found. Map features will be disabled.")
        if not cls.IMAGE_SEARCH_API_KEY:
            print("⚠️ Warning: IMAGE_SEARCH_API_KEY not found. Image features will be disabled.")
        
        return True
