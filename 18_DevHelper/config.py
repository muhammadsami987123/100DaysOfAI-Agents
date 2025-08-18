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
TEMPERATURE = float(get_env("TEMPERATURE", "0.3") or 0.3)
MAX_TOKENS = int(get_env("MAX_TOKENS", "800") or 800)
VOICE_INPUT = (get_env("VOICE_INPUT", "false") or "false").lower() == "true"

# Defaults for when the user does not specify names
DEFAULT_FILE_NAME = get_env("DEFAULT_FILE_NAME", "new_file.txt") or "new_file.txt"
DEFAULT_FOLDER_NAME = get_env("DEFAULT_FOLDER_NAME", "New Folder") or "New Folder"

# Conversation memory settings
MAX_HISTORY_MESSAGES = int(get_env("MAX_HISTORY_MESSAGES", "10") or 10)
