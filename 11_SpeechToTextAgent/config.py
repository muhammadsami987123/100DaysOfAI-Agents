import os
from dotenv import load_dotenv


load_dotenv()


def get_env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    return value


OPENAI_API_KEY = get_env("OPENAI_API_KEY")
WHISPER_MODEL = get_env("WHISPER_MODEL", "whisper-1")
PORT = int(get_env("PORT", "8010"))

# File size limits
MAX_FILE_SIZE = int(get_env("MAX_FILE_SIZE", "26214400"))  # 25MB in bytes

# Supported audio formats
SUPPORTED_AUDIO_FORMATS = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac"}

# Supported video formats
SUPPORTED_VIDEO_FORMATS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv"}

# Transcription settings
DEFAULT_LANGUAGE = "auto"  # Auto-detect language
INCLUDE_TIMESTAMPS = False  # Include timestamps in output
