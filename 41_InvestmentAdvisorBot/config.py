import os
from dotenv import load_dotenv

# Load .env if present
home = os.path.expanduser("~")
env_path = os.path.join(home, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def get_api_key():
    if OPENAI_API_KEY:
        return OPENAI_API_KEY
    return os.getenv('OPENAI_API_KEY')

def setup_instructions():
    print("InvestmentAdvisorBot Setup Instructions:\n")
    print("1) Create a .env file in your home directory with: OPENAI_API_KEY=your_key")
    print("2) Or set environment variable OPENAI_API_KEY before running the script.")
    print("3) Get your key from https://platform.openai.com/account/api-keys")
import os


class Config:
    """Simple configuration helper for InvestmentAdvisorBot."""
    OPENAI_API_KEY_ENV = "OPENAI_API_KEY"

    @staticmethod
    def get_api_key():
        return os.environ.get(Config.OPENAI_API_KEY_ENV)

    @staticmethod
    def setup_instructions():
        print("\nPlease set your OpenAI API key as an environment variable:")
        print(f"  setx {Config.OPENAI_API_KEY_ENV} \"<your_api_key>\"")
        print("Then restart your terminal.\n")
