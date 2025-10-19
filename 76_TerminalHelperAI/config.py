import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini").lower() # Default to gemini
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "1000"))
    
    DEFAULT_SHELL: str = os.getenv("DEFAULT_SHELL", "bash")
    SAFETY_MODE: bool = os.getenv("SAFETY_MODE", "true").lower() == "true"
    MAX_HISTORY_MESSAGES: int = int(os.getenv("MAX_HISTORY_MESSAGES", "10"))

    @classmethod
    def validate(cls):
        if cls.LLM_MODEL == "gemini":
            if not cls.GEMINI_API_KEY:
                print("Warning: GEMINI_API_KEY not found. AI features will be limited.")
                return False
        elif cls.LLM_MODEL == "openai":
            if not cls.OPENAI_API_KEY:
                print("Warning: OPENAI_API_KEY not found. AI features will be limited.")
                return False
        else:
            print("Warning: Invalid LLM_MODEL specified. Must be 'openai' or 'gemini'.")
            return False
        return True
