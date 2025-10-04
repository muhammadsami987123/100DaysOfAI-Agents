import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for AIQuoteGenerator Agent"""
    
    # Google Gemini Configuration
    GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-2.0-flash-001"
    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True
    
    # UI Configuration
    APP_TITLE = "AIQuoteGenerator"
    APP_DESCRIPTION = "Your daily spark, one quote at a time — generate inspirational quotes with AI."
    
    # Quote Generation Settings
    MOODS = ["Success", "Mindset", "Positivity", "Hustle", "Self-Reflection"]
    TONES = ["Poetic", "Bold", "Simple", "Deep"]
    OUTPUT_FORMATS = ["Text only", "Image Quote", "Tweet-ready"]
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        return True
