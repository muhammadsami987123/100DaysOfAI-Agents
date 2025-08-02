import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for Weather Speaker Agent"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o-mini"
    
    # Weather API Configuration
    WEATHER_API_BASE_URL = "https://api.open-meteo.com/v1"
    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True
    
    # TTS Configuration
    TTS_ENABLED = True
    TTS_LANGUAGE = "en"
    TTS_VOICE_RATE = 150
    
    # UI Configuration
    APP_TITLE = "Weather Speaker Agent"
    APP_DESCRIPTION = "AI-powered weather assistant with voice capabilities"
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        return True 