import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Default Models
    DEFAULT_MODEL_PROVIDER = os.getenv("DEFAULT_MODEL_PROVIDER", "gemini") # 'gemini' or 'openai'
    GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.0-flash")
    OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")

    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    # TTS Configuration
    TTS_ENGINE = os.getenv("TTS_ENGINE", "gtts") # 'gtts' or 'pyttsx3' (for offline fallback)
    AUDIO_DIR = "static/audio"

    # Prompt file path
    PROMPT_FILE = "prompts/motivation_prompt.txt"

    @classmethod
    def validate(cls):
        if cls.DEFAULT_MODEL_PROVIDER == "gemini" and not cls.GEMINI_API_KEY:
            print("Warning: GEMINI_API_KEY not found. Gemini model might not work.")
            return False
        if cls.DEFAULT_MODEL_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            print("Warning: OPENAI_API_KEY not found. OpenAI model might not work.")
            return False
        return True
