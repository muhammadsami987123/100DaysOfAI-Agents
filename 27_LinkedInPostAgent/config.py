import os
from pathlib import Path

from dotenv import load_dotenv


def load_env() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()


def get_openai_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY", "")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set in environment.")
    return key


def get_linkedin_method() -> str:
    # Supported: 'simulate', 'playwright'
    return os.getenv("LINKEDIN_METHOD", "simulate")


def get_timezone() -> str:
    return os.getenv("LOCAL_TIMEZONE", "local")


def get_linkedin_username() -> str:
    return os.getenv("LINKEDIN_USERNAME", "")


def get_linkedin_password() -> str:
    return os.getenv("LINKEDIN_PASSWORD", "")


