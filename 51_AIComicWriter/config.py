import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# --- OpenAI Configuration (for more advanced models or if preferred) ---
class OpenAIConfig:
    """OpenAI API configuration and client"""

    def __init__(self):
        self.api_key = self._get_api_key()
        self.client = None

        if self.api_key:
            # Only import openai if API key is present
            try:
                import openai
                openai.api_key = self.api_key
                self.client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                print("⚠️  OpenAI library not found. Please install it: pip install openai")
                self.client = None
            except Exception as e:
                print(f"⚠️  Error initializing OpenAI client: {e}")
                self.client = None
        else:
            print("⚠️  OpenAI API key not found. OpenAI features will be unavailable.")
            print("   Set OPENAI_API_KEY environment variable or create a .env file")

    def _get_api_key(self) -> Optional[str]:
        """Get OpenAI API key from environment or .env file"""
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            return api_key
        return None

    def is_available(self) -> bool:
        """Check if OpenAI API is available"""
        return self.client is not None

    def get_client(self):
        """Get OpenAI client instance"""
        return self.client

    def get_model(self) -> str:
        """Get OpenAI model name"""
        return os.getenv("OPENAI_MODEL", "gpt-3.5-turbo") # Using gpt-3.5-turbo as a default

    def get_temperature(self) -> float:
        """Get OpenAI temperature setting"""
        try:
            return float(os.getenv("TEMPERATURE", "0.7"))
        except ValueError:
            return 0.7

    def get_max_tokens(self) -> int:
        """Get OpenAI max tokens setting"""
        try:
            return int(os.getenv("MAX_TOKENS", "700")) # Adjusted max tokens for comic scripts
        except ValueError:
            return 700

    def get_env_variable(self, name: str, default: str) -> str:
        """Get environment variable with a default value"""
        return os.getenv(name, default)

OPENAI_CONFIG = OpenAIConfig()

# --- Hugging Face Transformers Configuration ---
from transformers import pipeline

def load_huggingface_pipeline():
    """Loads the Hugging Face text generation pipeline."""
    try:
        # Using a smaller, faster model for demonstration purposes.
        # For higher quality, consider larger models like "t5-large" or fine-tuned variants.
        generator = pipeline("text2text-generation", model="t5-small", device=-1)  # -1 for CPU, 0 for GPU
        return generator
    except Exception as e:
        print(f"Error loading Hugging Face pipeline: {e}")
        print("Please ensure you have \'transformers\' and \'torch\' installed.")
        print("You might also need to download the model, which requires an internet connection.")
        return None

HUGGINGFACE_PIPELINE = load_huggingface_pipeline()

def get_ai_backend(use_openai: bool = False):
    """Returns the appropriate AI backend based on configuration."""
    if use_openai and OPENAI_CONFIG.is_available():
        print("Using OpenAI backend.")
        return "openai", OPENAI_CONFIG.get_client(), OPENAI_CONFIG.get_model(), OPENAI_CONFIG.get_temperature(), OPENAI_CONFIG.get_max_tokens()
    elif HUGGINGFACE_PIPELINE is not None:
        print("Using Hugging Face backend.")
        return "huggingface", HUGGINGFACE_PIPELINE, None, None, None # Client, model, temp, max_tokens are not applicable for HF pipeline direct call
    else:
        print("No AI backend available. Please check your setup.")
        return "none", None, None, None, None
