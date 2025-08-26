import os
from dataclasses import dataclass

try:
	from dotenv import load_dotenv  # type: ignore
	load_dotenv()
except Exception:
	pass


@dataclass
class FocusTimerConfig:
	"""Configuration for FocusTimerAgent with sensible defaults."""
	default_work_minutes: int = 25
	default_short_break_minutes: int = 5
	default_long_break_minutes: int = 20
	cycles_before_long_break: int = 4
	voice_enabled: bool = True
	tts_rate: int = 180
	tts_volume: float = 1.0

	# File persistence
	data_dir: str = os.path.join(os.path.dirname(__file__), "data")
	state_file: str = os.path.join(data_dir, "state.json")
	history_file: str = os.path.join(data_dir, "history.json")

	# OpenAI
	openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
	openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


CONFIG = FocusTimerConfig()


