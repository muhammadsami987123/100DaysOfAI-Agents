import os
from pathlib import Path
try:
    from dotenv import load_dotenv  # type: ignore
except Exception:  # pragma: no cover
    load_dotenv = None  # type: ignore


# Base directory for this package
BASE_DIR = Path(__file__).resolve().parent

# Cache file location
CACHE_PATH = str(BASE_DIR / "cache.json")

# Load .env if available
if load_dotenv is not None:
    # load from project root if present
    root_env = Path(__file__).resolve().parent.parent / ".env"
    if root_env.exists():
        load_dotenv(dotenv_path=str(root_env))
    else:
        load_dotenv()

# exchangerate.host configuration
EXCHANGE_RATE_API_BASE = os.getenv("EXCHANGE_RATE_API_BASE", "https://api.exchangerate.host")
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY", "")

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_cache_path() -> str:
    return CACHE_PATH


def get_request_timeout() -> int:
    return REQUEST_TIMEOUT_SECONDS


def is_openai_enabled() -> bool:
    return bool(OPENAI_API_KEY)


