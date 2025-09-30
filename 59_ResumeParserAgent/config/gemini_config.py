import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class GeminiConfig:
    """Gemini API configuration and client"""

    def __init__(self):
        self.api_key = self._get_api_key()

        if not self.api_key:
            print("⚠️  Gemini API key not found. Some features may not work.")
            print("   Set GEMINI_API_KEY environment variable or create .env file")

    def _get_api_key(self) -> Optional[str]:
        """Get Gemini API key from environment or .env file"""
        api_key = os.getenv('GEMINI_API_KEY')
        return api_key

    def is_available(self) -> bool:
        """Check if Gemini API is available"""
        return self.api_key is not None

    def get_model_name(self) -> str:
        """Get Gemini model name"""
        return os.getenv("GEMINI_MODEL", "gemini-2.0-flash-001")

    def get_temperature(self) -> float:
        """Get Gemini temperature setting"""
        try:
            return float(os.getenv("TEMPERATURE", "0.7"))
        except ValueError:
            return 0.7

    def get_max_tokens(self) -> int:
        """Get Gemini max tokens setting"""
        try:
            return int(os.getenv("MAX_TOKENS", "1500"))
        except ValueError:
            return 1500

    def get_env_variable(self, name: str, default: str) -> str:
        """Get environment variable with a default value"""
        return os.getenv(name, default)
