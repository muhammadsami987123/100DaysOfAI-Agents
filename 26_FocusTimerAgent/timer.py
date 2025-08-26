from __future__ import annotations

import json
import os
import signal
import sys
import threading
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Optional

# Support running as a module or as a script
try:
	from .config import CONFIG
	from .tts_service import (
		TTSService,
		PHRASE_START_FOCUS,
		PHRASE_SHORT_BREAK,
		PHRASE_LONG_BREAK,
		PHRASE_END_BREAK,
	)
except Exception:  # pragma: no cover
	from config import CONFIG  # type: ignore
	from tts_service import (  # type: ignore
		TTSService,
		PHRASE_START_FOCUS,
		PHRASE_SHORT_BREAK,
		PHRASE_LONG_BREAK,
		PHRASE_END_BREAK,
	)


def _ensure_data_dir() -> None:
	os.makedirs(CONFIG.data_dir, exist_ok=True)


def _read_json(path: str) -> Dict:
	if not os.path.exists(path):
		return {}
	try:
		with open(path, "r", encoding="utf-8") as f:
			return json.load(f)
	except Exception:
		return {}


def _write_json(path: str, data: Dict) -> None:
	with open(path, "w", encoding="utf-8") as f:
		json.dump(data, f, indent=2)


@dataclass
class TimerState:
	mode: str  # focus | short_break | long_break | idle
	current_cycle: int
	session_seconds_remaining: int
	is_paused: bool
	voice_enabled: bool
	command: Optional[str] = None  # pause|resume|stop|mute|unmute


class PomodoroTimer:
	"""Core Pomodoro timer with state persistence and command handling via state file."""

	def __init__(
		self,
		work_minutes: int = CONFIG.default_work_minutes,
		short_break_minutes: int = CONFIG.default_short_break_minutes,
		long_break_minutes: int = CONFIG.default_long_break_minutes,
		cycles_before_long: int = CONFIG.cycles_before_long_break,
		voice_enabled: bool = CONFIG.voice_enabled,
	) -> None:
		_ensure_data_dir()
		self.work_seconds = max(1, work_minutes) * 60
		self.short_break_seconds = max(1, short_break_minutes) * 60
		self.long_break_seconds = max(1, long_break_minutes) * 60
		self.cycles_before_long = max(1, cycles_before_long)
		self.state = TimerState(
			mode="idle",
			current_cycle=0,
			session_seconds_remaining=self.work_seconds,
			is_paused=False,
			voice_enabled=voice_enabled,
			command=None,
		)
		self.tts = TTSService(enabled=voice_enabled)
		self._write_state()

	def _write_state(self) -> None:
		_write_json(CONFIG.state_file, asdict(self.state))

	def _read_state_for_commands(self) -> None:
		data = _read_json(CONFIG.state_file)
		cmd = data.get("command") if isinstance(data, dict) else None
		if cmd:
			self.state.command = cmd

	def _apply_command(self) -> bool:
		cmd = self.state.command
		if not cmd:
			return True
		self.state.command = None
		if cmd == "pause":
			self.state.is_paused = True
		elif cmd == "resume":
			self.state.is_paused = False
		elif cmd == "stop":
			self.state.mode = "idle"
			self._write_state()
			return False
		elif cmd == "mute":
			self.state.voice_enabled = False
			self.tts.set_enabled(False)
		elif cmd == "unmute":
			self.state.voice_enabled = True
			self.tts.set_enabled(True)
		self._write_state()
		return True

	def _log_session_completion(self) -> None:
		data = _read_json(CONFIG.history_file)
		day_key = datetime.now().strftime("%Y-%m-%d")
		day = data.get(day_key, {"completed_focus_sessions": 0})
		day["completed_focus_sessions"] = int(day.get("completed_focus_sessions", 0)) + 1
		data[day_key] = day
		_write_json(CONFIG.history_file, data)

	def _announce(self, text: str) -> None:
		self.tts.speak(text)

	def run(self) -> None:
		# Initial transition to focus mode
		self.state.mode = "focus"
		self.state.session_seconds_remaining = self.work_seconds
		self._write_state()
		self._announce(PHRASE_START_FOCUS)

		try:
			while True:
				self._read_state_for_commands()
				if not self._apply_command():
					break

				if self.state.is_paused:
					time.sleep(0.25)
					continue

				if self.state.session_seconds_remaining > 0:
					time.sleep(1)
					self.state.session_seconds_remaining -= 1
					if self.state.session_seconds_remaining % 5 == 0:
						self._write_state()
					continue

				# Session ended, transition
				if self.state.mode == "focus":
					self._log_session_completion()
					self.state.current_cycle += 1
					if self.state.current_cycle % self.cycles_before_long == 0:
						self.state.mode = "long_break"
						self.state.session_seconds_remaining = self.long_break_seconds
						self._write_state()
						self._announce(PHRASE_LONG_BREAK)
					else:
						self.state.mode = "short_break"
						self.state.session_seconds_remaining = self.short_break_seconds
						self._write_state()
						self._announce(PHRASE_SHORT_BREAK)
				elif self.state.mode in ("short_break", "long_break"):
					self.state.mode = "focus"
					self.state.session_seconds_remaining = self.work_seconds
					self._write_state()
					self._announce(PHRASE_END_BREAK)
				else:
					self.state.mode = "focus"
					self.state.session_seconds_remaining = self.work_seconds
					self._write_state()
					self._announce(PHRASE_START_FOCUS)
		except KeyboardInterrupt:
			self.state.mode = "idle"
			self._write_state()
			return


def read_status() -> Dict:
	_ensure_data_dir()
	state = _read_json(CONFIG.state_file)
	if not state:
		return {
			"mode": "idle",
			"current_cycle": 0,
			"session_seconds_remaining": 0,
			"is_paused": False,
			"voice_enabled": CONFIG.voice_enabled,
		}
	return state


def write_command(command: str) -> None:
	_ensure_data_dir()
	state = read_status()
	state["command"] = command
	_write_json(CONFIG.state_file, state)


def read_history() -> Dict:
	_ensure_data_dir()
	return _read_json(CONFIG.history_file)


