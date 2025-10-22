import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for GPTNotepad"""

    # API Configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini") # gemini or openai (gemini is default)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    # Server Configuration
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    # App Configuration
    APP_TITLE = "GPTNotepad"
    APP_DESCRIPTION = "Intelligent notepad with auto summaries"
    APP_VERSION = "1.0.0"

    # Summarizer Prompt
    SUMMARIZER_PROMPT_PATH = "prompts/summarizer_prompt.txt"

    @classmethod
    def validate(cls):
        """Validate required configuration"""
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
