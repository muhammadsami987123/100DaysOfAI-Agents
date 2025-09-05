"""
OpenAI configuration and API client setup
"""

import os
import openai
from typing import Optional


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
        # Try environment variable first
        api_key = os.getenv('OPENAI_API_KEY')
        
        if api_key:
            return api_key
        
        # Try .env file
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
