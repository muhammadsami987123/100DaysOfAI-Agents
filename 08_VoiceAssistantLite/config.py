import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


# Load .env from this directory if present
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


@dataclass
class AppConfig:
    stt_provider: str = os.getenv("STT_PROVIDER", "google").strip().lower()
    language: str = os.getenv("LANGUAGE", "en-US").strip()
    log_enabled: bool = os.getenv("LOG_ENABLED", "true").strip().lower() == "true"
    log_format: str = os.getenv("LOG_FORMAT", "jsonl").strip().lower()  # jsonl | csv
    log_file: str = os.getenv("LOG_FILE", str(BASE_DIR / "logs" / "qa_log.jsonl"))
    tts_rate: int = int(os.getenv("TTS_RATE", "170"))
    # Whisper
    whisper_model: str = os.getenv("WHISPER_MODEL", "base")
    whisper_device: str = os.getenv("WHISPER_DEVICE", "cpu")
    # FAQ
    faqs_path: str = os.getenv("FAQS_PATH", str(BASE_DIR / "faqs.json"))
    # OpenAI Assistants API
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    assistant_id: str = os.getenv("ASSISTANT_ID", "")
    assistant_instructions: str = os.getenv(
        "ASSISTANT_INSTRUCTIONS",
        (
            "You are a helpful, concise voice assistant. Answer clearly and accurately. "
            "Prefer short, direct answers suitable for TTS playback."
        ),
    )


def ensure_directories(config: AppConfig) -> None:
    log_path = Path(config.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)


CONFIG = AppConfig()
ensure_directories(CONFIG)


