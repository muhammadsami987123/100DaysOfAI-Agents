import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


@dataclass
class AppConfig:
    provider: str = os.getenv("PROVIDER", "languagetool").strip().lower()  # languagetool | openai
    language: str = os.getenv("LANGUAGE", "auto").strip()  # e.g., en-US, auto
    style: str = os.getenv("STYLE", "neutral").strip().lower()  # neutral | formal | casual
    hotkey: str = os.getenv("HOTKEY", "<ctrl>+.").strip()
    undo_hotkey: str = os.getenv("UNDO_HOTKEY", "<ctrl>+<shift>+w").strip()
    copy_wait_ms: int = int(os.getenv("COPY_WAIT_MS", "80"))
    paste_wait_ms: int = int(os.getenv("PASTE_WAIT_MS", "60"))
    log_enabled: bool = os.getenv("LOG_ENABLED", "true").strip().lower() == "true"
    restore_clipboard: bool = os.getenv("RESTORE_CLIPBOARD", "true").strip().lower() == "true"
    toast_enabled: bool = os.getenv("TOAST_ENABLED", "true").strip().lower() == "true"
    toast_duration_ms: int = int(os.getenv("TOAST_DURATION_MS", "800"))

    # LanguageTool HTTP API
    languagetool_url: str = os.getenv("LANGUAGETOOL_URL", "https://api.languagetool.org/v2/check").strip()

    # OpenAI
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()


CONFIG = AppConfig()


