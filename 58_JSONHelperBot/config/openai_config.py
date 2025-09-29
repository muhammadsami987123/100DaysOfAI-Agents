import os
import openai
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class OpenAIConfig:
    """OpenAI API configuration and client"""

    def __init__(self):
        self.api_key = self._get_api_key()
        self.client = None

        if self.api_key:
            openai.api_key = self.api_key
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            print("⚠️  OpenAI API key not found. Some features may not work.")
            print("   Set OPENAI_API_KEY environment variable or create .env file")

    def _get_api_key(self) -> Optional[str]:
        """Get OpenAI API key from environment or .env file"""
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            return api_key

        env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_file):
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith('OPENAI_API_KEY='):
                            return line.split('=', 1)[1].strip()
            except Exception:
                pass
        return None

    def is_available(self) -> bool:
        """Check if OpenAI API is available"""
        return self.client is not None

    def get_client(self):
        """Get OpenAI client instance"""
        return self.client

    def get_model(self) -> str:
        """Get OpenAI model name"""
        return os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def get_temperature(self) -> float:
        """Get OpenAI temperature setting"""
        try:
            return float(os.getenv("TEMPERATURE", "0.7"))
        except ValueError:
            return 0.7

    def get_max_tokens(self) -> int:
        """Get OpenAI max tokens setting"""
        try:
            return int(os.getenv("MAX_TOKENS", "1500"))
        except ValueError:
            return 1500

    def get_env_variable(self, name: str, default: str) -> str:
        """Get environment variable with a default value"""
        return os.getenv(name, default)
