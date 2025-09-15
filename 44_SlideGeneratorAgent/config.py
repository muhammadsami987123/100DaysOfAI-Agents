from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Settings:
    openai_api_key: str = os.environ.get("OPENAI_API_KEY", "")
    model: str = os.environ.get("SLIDES_MODEL", "gpt-4o-mini")
    host: str = os.environ.get("HOST", "0.0.0.0")
    port: int = int(os.environ.get("PORT", "8080"))
    slides_min: int = int(os.environ.get("SLIDES_MIN", "20"))
    slides_max: int = int(os.environ.get("SLIDES_MAX", "22"))
    include_images: bool = os.environ.get("INCLUDE_IMAGES", "true").lower() in {"1", "true", "yes", "on"}
    download_images: bool = os.environ.get("DOWNLOAD_IMAGES", "true").lower() in {"1", "true", "yes", "on"}
    image_timeout_sec: int = int(os.environ.get("IMAGE_TIMEOUT_SEC", "10"))


# Load .env (if present) before building settings
load_dotenv()
CONFIG = Settings(
    openai_api_key=os.environ.get("OPENAI_API_KEY", ""),
    model=os.environ.get("SLIDES_MODEL", "gpt-4o-mini"),
    host=os.environ.get("HOST", "0.0.0.0"),
    port=int(os.environ.get("PORT", "8080")),
    slides_min=int(os.environ.get("SLIDES_MIN", "20")),
    slides_max=int(os.environ.get("SLIDES_MAX", "22")),
    include_images=os.environ.get("INCLUDE_IMAGES", "true").lower() in {"1", "true", "yes", "on"},
    download_images=os.environ.get("DOWNLOAD_IMAGES", "false").lower() in {"1", "true", "yes", "on"},
    image_timeout_sec=int(os.environ.get("IMAGE_TIMEOUT_SEC", "10")),
)


