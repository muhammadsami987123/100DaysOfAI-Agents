from __future__ import annotations

import os
from dataclasses import dataclass

try:
	from dotenv import load_dotenv
	load_dotenv()
except Exception:
	pass


@dataclass
class _Config:
	host: str = os.getenv("HOST", "127.0.0.1")
	port: int = int(os.getenv("PORT", "8022"))
	debug: bool = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")
	openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
	openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini-transcribe")
	use_real_transcription: bool = os.getenv("USE_REAL_TRANSCRIPTION", "false").lower() in ("1", "true", "yes")
	request_timeout_sec: int = int(os.getenv("REQUEST_TIMEOUT_SEC", "60"))
	# youtube
	enable_youtube: bool = os.getenv("ENABLE_YOUTUBE", "false").lower() in ("1", "true", "yes")
	tmp_dir: str = os.getenv("TMP_DIR", os.path.join(os.path.dirname(__file__), "tmp"))
	# storage
	base_dir: str = os.path.dirname(__file__)
	subtitles_dir: str = os.path.join(base_dir, "subtitles")
	static_dir: str = os.path.join(base_dir, "static")
	templates_dir: str = os.path.join(base_dir, "templates")


CONFIG = _Config()
