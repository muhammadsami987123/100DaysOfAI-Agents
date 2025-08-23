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
MAX_TOKENS = int(get_env("MAX_TOKENS", "1000") or 1000)

# Command explanation settings
MAX_HISTORY_MESSAGES = int(get_env("MAX_HISTORY_MESSORIES", "8") or 8)
DANGEROUS_COMMANDS = [
    "rm -rf", "rm -rf /", "rm -rf /*", "rm -rf /home", "rm -rf /etc",
    ":(){ :|:& };:", "fork()", "dd if=/dev/zero", "mkfs", "fdisk",
    "chmod 777", "chmod -R 777", "chown root", "chown -R root",
    "sudo rm", "sudo chmod", "sudo chown", "sudo mkfs",
    "del /s /q", "rmdir /s /q", "format", "diskpart"
]
