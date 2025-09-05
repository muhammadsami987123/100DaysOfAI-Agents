import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    return value

OPENAI_API_KEY = get_env("OPENAI_API_KEY")
OPENAI_MODEL = get_env("OPENAI_MODEL", "gpt-4o-mini") or "gpt-4o-mini"
TEMPERATURE = float(get_env("TEMPERATURE", "0.1") or 0.1)
MAX_TOKENS = int(get_env("MAX_TOKENS", "400") or 400)

# TerminalGPT specific settings
DEFAULT_SHELL = get_env("DEFAULT_SHELL", "bash") or "bash"
SAFETY_MODE = (get_env("SAFETY_MODE", "true") or "true").lower() == "true"
MAX_HISTORY_MESSAGES = int(get_env("MAX_HISTORY_MESSAGES", "6") or 6)
