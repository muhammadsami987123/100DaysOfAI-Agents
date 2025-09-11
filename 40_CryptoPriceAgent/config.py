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
PORTFOLIO_PATH = str(BASE_DIR / "portfolio.json")

# Load .env if available
if load_dotenv is not None:
    # load from project root if present
    root_env = Path(__file__).resolve().parent.parent / ".env"
    if root_env.exists():
        load_dotenv(dotenv_path=str(root_env))
    else:
        load_dotenv()

# CoinGecko API configuration
COINGECKO_API_BASE = os.getenv("COINGECKO_API_BASE", "https://api.coingecko.com/api/v3")
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Default settings
DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "usd")
DEFAULT_CRYPTOS = ["bitcoin", "ethereum", "binancecoin", "cardano", "solana", "polkadot", "dogecoin", "chainlink"]


def get_cache_path() -> str:
    return CACHE_PATH


def get_portfolio_path() -> str:
    return PORTFOLIO_PATH


def get_request_timeout() -> int:
    return REQUEST_TIMEOUT_SECONDS


def is_openai_enabled() -> bool:
    return bool(OPENAI_API_KEY)


def get_default_currency() -> str:
    return DEFAULT_CURRENCY


def get_default_cryptos() -> list:
    return DEFAULT_CRYPTOS
