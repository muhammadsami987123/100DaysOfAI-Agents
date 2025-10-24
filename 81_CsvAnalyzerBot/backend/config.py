import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))

    UPLOAD_DIR = "uploads"
    CHARTS_DIR = "charts"
    
    @classmethod
    def validate(cls):
        if cls.LLM_MODEL.lower() == "gemini":
            if not cls.GEMINI_API_KEY:
                print("⚠️ Warning: GEMINI_API_KEY not found. AI features will be limited.")
                return False
        elif cls.LLM_MODEL.lower() == "openai":
            if not cls.OPENAI_API_KEY:
                print("⚠️ Warning: OPENAI_API_KEY not found. AI features will be limited.")
                return False
        else:
            print("⚠️ Warning: No valid LLM model configured. AI features will be limited.")
            return False
        return True
