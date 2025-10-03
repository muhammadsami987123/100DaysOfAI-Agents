import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment variable with a default value."""
    value = os.getenv(name)
    return value if value is not None else default

# GitHub Configuration
GITHUB_TOKEN: Optional[str] = get_env("GITHUB_TOKEN")

# Default behavior
DEFAULT_BRANCH: str = get_env("DEFAULT_BRANCH", "main") or "main"

# Logging configuration
LOG_LEVEL: str = get_env("LOG_LEVEL", "INFO") or "INFO"
