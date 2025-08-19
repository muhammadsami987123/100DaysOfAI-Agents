import os
from typing import Optional, List
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    return value


# OpenAI configuration
OPENAI_API_KEY: Optional[str] = get_env("OPENAI_API_KEY")
OPENAI_MODEL: str = get_env("OPENAI_MODEL", "gpt-4o-mini") or "gpt-4o-mini"
TEMPERATURE: float = float(get_env("TEMPERATURE", "0.5") or 0.5)
MAX_TOKENS: int = int(get_env("MAX_TOKENS", "800") or 800)
STREAMING: bool = (get_env("STREAMING", "true") or "true").lower() == "true"

# Memory configuration (per conversation thread)
MAX_TURNS_PER_THREAD: int = int(get_env("MAX_TURNS_PER_THREAD", "100") or 100)

# Default behavior
DEFAULT_TONE: str = get_env("DEFAULT_TONE", "friendly") or "friendly"  # friendly | formal | technical | concise
DEFAULT_LANGUAGE: str = get_env("DEFAULT_LANGUAGE", "auto") or "auto"  # auto or ISO language like en, ur, hi

# Message source configuration
SOURCE_TYPE: str = get_env("SOURCE_TYPE", "json") or "json"  # json | inbox | chat (custom integrations can map to json)
DATA_DIR: str = get_env("DATA_DIR", os.path.join(os.path.dirname(__file__), "data")) or os.path.join(os.path.dirname(__file__), "data")
INBOX_JSON_PATH: str = get_env("INBOX_JSON_PATH", os.path.join(DATA_DIR, "inbox.json")) or os.path.join(DATA_DIR, "inbox.json")
CHAT_JSON_PATH: str = get_env("CHAT_JSON_PATH", os.path.join(DATA_DIR, "chat_log.json")) or os.path.join(DATA_DIR, "chat_log.json")
OUTBOX_JSON_PATH: str = get_env("OUTBOX_JSON_PATH", os.path.join(DATA_DIR, "outbox.json")) or os.path.join(DATA_DIR, "outbox.json")

# Auto-mode controls
AUTO_MODE_DELAY_SECONDS: float = float(get_env("AUTO_MODE_DELAY_SECONDS", "2.0") or 2.0)

# Filters
KEYWORDS: List[str] = [
    kw.strip() for kw in (get_env("KEYWORDS", "urgent, asap, follow up, inquiry") or "").split(",") if kw.strip()
]
BLACKLIST_CONTACTS: List[str] = [
    x.strip().lower() for x in (get_env("BLACKLIST_CONTACTS", "no-reply@, donotreply@") or "").split(",") if x.strip()
]

# Optional add-ons
SCHEDULE_ENABLED: bool = (get_env("SCHEDULE_ENABLED", "false") or "false").lower() == "true"
VOICE_ENABLED: bool = (get_env("VOICE_ENABLED", "false") or "false").lower() == "true"

# Gmail integration (optional)
GMAIL_ENABLED: bool = (get_env("GMAIL_ENABLED", "false") or "false").lower() == "true"
GMAIL_QUERY: str = get_env("GMAIL_QUERY", "is:unread -category:promotions -category:social") or "is:unread -category:promotions -category:social"
GMAIL_MAX_RESULTS: int = int(get_env("GMAIL_MAX_RESULTS", "20") or 20)
GMAIL_CREDENTIALS_FILE: str = get_env("GMAIL_CREDENTIALS_FILE", os.path.join(DATA_DIR, "credentials.json")) or os.path.join(DATA_DIR, "credentials.json")
GMAIL_TOKEN_FILE: str = get_env("GMAIL_TOKEN_FILE", os.path.join(DATA_DIR, "token.json")) or os.path.join(DATA_DIR, "token.json")
GMAIL_USER: str = get_env("GMAIL_USER", "me") or "me"


