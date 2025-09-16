from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class CONFIG:
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8015"))
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"

    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # limits
    max_image_bytes: int = 8 * 1024 * 1024  # 8MB
    allowed_exts: tuple[str, ...] = (".jpg", ".jpeg", ".png", ".webp")


