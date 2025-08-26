from __future__ import annotations

import threading
from typing import Optional

# Support running as a module or as a script
try:
	from .config import CONFIG
except Exception:  # pragma: no cover
	from config import CONFIG  # type: ignore

try:
	import pyttsx3
except Exception:  # pragma: no cover - optional dependency during tests
	pyttsx3 = None  # type: ignore


class TTSService:
	"""Simple wrapper around pyttsx3 with mute support."""

	def __init__(self, enabled: bool = CONFIG.voice_enabled) -> None:
		self._enabled = enabled
		self._engine = None  # lazy init
		self._lock = threading.Lock()

	def _ensure_engine(self) -> None:
		if not self._enabled:
			return
		if self._engine is None and pyttsx3 is not None:
			self._engine = pyttsx3.init()
			self._engine.setProperty("rate", CONFIG.tts_rate)
			self._engine.setProperty("volume", CONFIG.tts_volume)

	def set_enabled(self, enabled: bool) -> None:
		with self._lock:
			self._enabled = enabled

	def speak(self, text: str) -> None:
		if not self._enabled or not text:
			return
		self._ensure_engine()
		if self._engine is None:
			return
		with self._lock:
			self._engine.say(text)
			self._engine.runAndWait()


# Common phrases
PHRASE_START_FOCUS = "Time to focus."
PHRASE_SHORT_BREAK = "Break time! You've earned it."
PHRASE_LONG_BREAK = "Take a longer break now."
PHRASE_END_BREAK = "Let's get back to work."


