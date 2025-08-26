from __future__ import annotations

import os
import sys
import importlib.util
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

def _resource_base() -> str:
	# Support PyInstaller onefile via sys._MEIPASS and normal execution via __file__
	if hasattr(sys, "_MEIPASS"):
		return getattr(sys, "_MEIPASS")  # type: ignore
	return os.path.dirname(os.path.abspath(__file__))


def _import_local(module_filename: str):
	base = _resource_base()
	path = os.path.join(base, module_filename)
	if not os.path.exists(path):
		raise ImportError(f"Local module not found: {module_filename}")
	spec = importlib.util.spec_from_file_location(module_filename.replace(".py", ""), path)
	if spec is None or spec.loader is None:
		raise ImportError(f"Unable to load spec for {module_filename}")
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


# Try package-relative imports first; fallback to loading local modules by path
try:
	from .config import CONFIG
	from .tts_service import (
		TTSService,
		PHRASE_START_FOCUS,
		PHRASE_SHORT_BREAK,
		PHRASE_LONG_BREAK,
		PHRASE_END_BREAK,
	)
except Exception:
	_config = _import_local("config.py")
	CONFIG = getattr(_config, "CONFIG")
	_tts = _import_local("tts_service.py")
	TTSService = getattr(_tts, "TTSService")
	PHRASE_START_FOCUS = getattr(_tts, "PHRASE_START_FOCUS")
	PHRASE_SHORT_BREAK = getattr(_tts, "PHRASE_SHORT_BREAK")
	PHRASE_LONG_BREAK = getattr(_tts, "PHRASE_LONG_BREAK")
	PHRASE_END_BREAK = getattr(_tts, "PHRASE_END_BREAK")


def ensure_data_dir() -> None:
	os.makedirs(CONFIG.data_dir, exist_ok=True)


def read_json(path: str) -> dict:
	if not os.path.exists(path):
		return {}
	try:
		import json
		with open(path, "r", encoding="utf-8") as f:
			return json.load(f)
	except Exception:
		return {}


def write_json(path: str, data: dict) -> None:
	import json
	with open(path, "w", encoding="utf-8") as f:
		json.dump(data, f, indent=2)


def notify(title: str, message: str) -> None:
	"""Best-effort system notification."""
	try:
		from plyer import notification  # type: ignore
		notification.notify(title=title, message=message, timeout=5)
	except Exception:
		# Fallback to messagebox if GUI-focused
		try:
			messagebox.showinfo(title, message)
		except Exception:
			pass


def play_chime() -> None:
	"""Play a simple chime on Windows; ignore elsewhere."""
	try:
		import winsound  # type: ignore
		winsound.Beep(880, 200)
		winsound.Beep(988, 200)
		winsound.Beep(1046, 300)
	except Exception:
		pass


class PomodoroGUI(tk.Tk):
	def __init__(self) -> None:
		super().__init__()
		self.title("FocusTimerAgent")
		self.geometry("520x420")
		self.minsize(480, 380)

		ensure_data_dir()
		self.tts = TTSService(enabled=CONFIG.voice_enabled)

		self.work_minutes_var = tk.IntVar(value=CONFIG.default_work_minutes)
		self.work_seconds_var = tk.IntVar(value=0)
		self.short_break_minutes_var = tk.IntVar(value=CONFIG.default_short_break_minutes)
		self.short_break_seconds_var = tk.IntVar(value=0)
		self.long_break_minutes_var = tk.IntVar(value=CONFIG.default_long_break_minutes)
		self.long_break_seconds_var = tk.IntVar(value=0)
		self.cycles_before_long_var = tk.IntVar(value=CONFIG.cycles_before_long_break)
		self.voice_enabled_var = tk.BooleanVar(value=CONFIG.voice_enabled)

		self.mode = "idle"  # idle|focus|short_break|long_break
		self.seconds_remaining = 0
		self.completed_cycles = 0
		self.is_running = False
		self.is_paused = False

		self._build_ui()
		self._update_status()

	def _build_ui(self) -> None:
		pad = 8
		frm_top = ttk.Frame(self)
		frm_top.pack(fill=tk.X, padx=pad, pady=pad)

		# Settings row
		row1 = ttk.Frame(frm_top)
		row1.pack(fill=tk.X, pady=(0, 4))
		ttk.Label(row1, text="Work").pack(side=tk.LEFT)
		spn_work_m = ttk.Spinbox(row1, from_=0, to=180, textvariable=self.work_minutes_var, width=4)
		spn_work_m.pack(side=tk.LEFT, padx=(4, 2))
		ttk.Label(row1, text="m").pack(side=tk.LEFT)
		spn_work_s = ttk.Spinbox(row1, from_=0, to=59, textvariable=self.work_seconds_var, width=4)
		spn_work_s.pack(side=tk.LEFT, padx=(4, 10))
		ttk.Label(row1, text="s").pack(side=tk.LEFT)

		ttk.Label(row1, text="Break").pack(side=tk.LEFT)
		spn_break_m = ttk.Spinbox(row1, from_=0, to=60, textvariable=self.short_break_minutes_var, width=4)
		spn_break_m.pack(side=tk.LEFT, padx=(4, 2))
		ttk.Label(row1, text="m").pack(side=tk.LEFT)
		spn_break_s = ttk.Spinbox(row1, from_=0, to=59, textvariable=self.short_break_seconds_var, width=4)
		spn_break_s.pack(side=tk.LEFT, padx=(4, 10))
		ttk.Label(row1, text="s").pack(side=tk.LEFT)

		ttk.Label(row1, text="Long").pack(side=tk.LEFT)
		spn_long_m = ttk.Spinbox(row1, from_=0, to=120, textvariable=self.long_break_minutes_var, width=4)
		spn_long_m.pack(side=tk.LEFT, padx=(4, 2))
		ttk.Label(row1, text="m").pack(side=tk.LEFT)
		spn_long_s = ttk.Spinbox(row1, from_=0, to=59, textvariable=self.long_break_seconds_var, width=4)
		spn_long_s.pack(side=tk.LEFT, padx=(4, 10))
		ttk.Label(row1, text="s").pack(side=tk.LEFT)

		ttk.Label(row1, text="Cycles/Long").pack(side=tk.LEFT)
		spn_cycles = ttk.Spinbox(row1, from_=1, to=12, textvariable=self.cycles_before_long_var, width=5)
		spn_cycles.pack(side=tk.LEFT, padx=(4, 0))

		# Presets and Countdown display
		frm_mid = ttk.Frame(self)
		frm_mid.pack(fill=tk.BOTH, expand=True, padx=pad, pady=(0, pad))
		preset_row = ttk.Frame(frm_mid)
		preset_row.pack(fill=tk.X)
		self.preset_var = tk.StringVar(value="Custom")
		preset = ttk.Combobox(preset_row, textvariable=self.preset_var, values=["Custom","Pomodoro (25/5)","Long Focus (50/10)","Quick (15/3)"], state="readonly", width=24)
		preset.pack(side=tk.LEFT)
		preset.bind("<<ComboboxSelected>>", self._on_preset)
		btn_reset = ttk.Button(preset_row, text="Reset", command=self._reset_timer)
		btn_reset.pack(side=tk.LEFT, padx=(6,0))

		self.timer_label = ttk.Label(frm_mid, text="00:00", font=("Segoe UI", 36))
		self.timer_label.pack(pady=(8, 6))
		self.mode_label = ttk.Label(frm_mid, text="Idle", font=("Segoe UI", 12))
		self.mode_label.pack()

		self.progress = ttk.Progressbar(frm_mid, orient="horizontal", mode="determinate")
		self.progress.pack(fill=tk.X, padx=pad, pady=(6, 0))

		# Controls
		frm_ctrl = ttk.Frame(self)
		frm_ctrl.pack(fill=tk.X, padx=pad, pady=pad)
		self.btn_start = ttk.Button(frm_ctrl, text="Start", command=self.on_start)
		self.btn_start.pack(side=tk.LEFT)
		self.btn_pause = ttk.Button(frm_ctrl, text="Pause", command=self.on_pause, state=tk.DISABLED)
		self.btn_pause.pack(side=tk.LEFT, padx=(6, 0))
		self.btn_resume = ttk.Button(frm_ctrl, text="Resume", command=self.on_resume, state=tk.DISABLED)
		self.btn_resume.pack(side=tk.LEFT, padx=(6, 0))
		self.btn_stop = ttk.Button(frm_ctrl, text="Stop", command=self.on_stop, state=tk.DISABLED)
		self.btn_stop.pack(side=tk.LEFT, padx=(6, 0))

		# Voice toggle
		chk_voice = ttk.Checkbutton(frm_ctrl, text="Voice", variable=self.voice_enabled_var, command=self.on_voice_toggle)
		chk_voice.pack(side=tk.RIGHT)

		# History area
		frm_hist = ttk.LabelFrame(self, text="Today's Sessions")
		frm_hist.pack(fill=tk.BOTH, expand=False, padx=pad, pady=(0, pad))
		self.history_list = tk.Listbox(frm_hist, height=5)
		self.history_list.pack(fill=tk.BOTH, expand=True, padx=pad, pady=(4, 6))
		self._load_history_into_listbox()

	def _load_history_into_listbox(self) -> None:
		data = read_json(CONFIG.history_file)
		self.history_list.delete(0, tk.END)
		if not data:
			return
		for day, info in sorted(data.items()):
			self.history_list.insert(tk.END, f"{day}: {info.get('completed_focus_sessions', 0)} focus sessions")

	def on_voice_toggle(self) -> None:
		enabled = bool(self.voice_enabled_var.get())
		self.tts.set_enabled(enabled)

	def on_start(self) -> None:
		if self.is_running:
			return
		self.is_running = True
		self.is_paused = False
		self.completed_cycles = 0
		self.mode = "focus"
		self.seconds_remaining = max(1, int(self.work_minutes_var.get()) * 60 + int(self.work_seconds_var.get()))
		self._announce_async(PHRASE_START_FOCUS)
		self._show_notification("FocusTimer", "Session started. Time to focus.")
		self._update_controls()
		self._tick()

	def on_pause(self) -> None:
		if not self.is_running:
			return
		self.is_paused = True
		self._update_controls()

	def on_resume(self) -> None:
		if not self.is_running:
			return
		self.is_paused = False
		self._update_controls()

	def on_stop(self) -> None:
		self.is_running = False
		self.is_paused = False
		self.mode = "idle"
		self.seconds_remaining = 0
		self._update_controls()
		self._update_status()

	def _update_controls(self) -> None:
		self.btn_start.configure(state=tk.DISABLED if self.is_running else tk.NORMAL)
		self.btn_pause.configure(state=tk.NORMAL if self.is_running and not self.is_paused else tk.DISABLED)
		self.btn_resume.configure(state=tk.NORMAL if self.is_running and self.is_paused else tk.DISABLED)
		self.btn_stop.configure(state=tk.NORMAL if self.is_running else tk.DISABLED)

	def _update_status(self) -> None:
		m = self.seconds_remaining // 60
		s = self.seconds_remaining % 60
		self.timer_label.configure(text=f"{m:02d}:{s:02d}")
		self.mode_label.configure(text=f"Mode: {self.mode.capitalize()} | Cycle: {self.completed_cycles}")
		# Update progress value
		if self.mode == "focus":
			total = max(1, int(self.work_minutes_var.get()) * 60 + int(self.work_seconds_var.get()))
		elif self.mode == "short_break":
			total = max(1, int(self.short_break_minutes_var.get()) * 60 + int(self.short_break_seconds_var.get()))
		elif self.mode == "long_break":
			total = max(1, int(self.long_break_minutes_var.get()) * 60 + int(self.long_break_seconds_var.get()))
		else:
			total = 1
		progress_value = 0 if total == 0 else 100 * (1 - (self.seconds_remaining / total))
		self.progress['value'] = progress_value

	def _tick(self) -> None:
		if not self.is_running:
			return
		if self.is_paused:
			self.after(300, self._tick)
			return

		if self.seconds_remaining > 0:
			self.seconds_remaining -= 1
			self._update_status()
			self.after(1000, self._tick)
			return

		# Transition
		if self.mode == "focus":
			self._log_session()
			self.completed_cycles += 1
			if self.completed_cycles % max(1, int(self.cycles_before_long_var.get())) == 0:
				self.mode = "long_break"
				self.seconds_remaining = max(1, int(self.long_break_minutes_var.get()) * 60 + int(self.long_break_seconds_var.get()))
				self._announce_async(PHRASE_LONG_BREAK)
				self._show_notification("FocusTimer", "Long break started.")
			else:
				self.mode = "short_break"
				self.seconds_remaining = max(1, int(self.short_break_minutes_var.get()) * 60 + int(self.short_break_seconds_var.get()))
				self._announce_async(PHRASE_SHORT_BREAK)
				self._show_notification("FocusTimer", "Break time! You've earned it.")
			play_chime()
		elif self.mode in ("short_break", "long_break"):
			self.mode = "focus"
			self.seconds_remaining = max(1, int(self.work_minutes_var.get()) * 60 + int(self.work_seconds_var.get()))
			self._announce_async(PHRASE_END_BREAK)
			self._show_notification("FocusTimer", "Break over, back to work!")

		self._update_status()
		self.after(1000, self._tick)

	def _announce_async(self, text: str) -> None:
		if not text:
			return
		threading.Thread(target=self.tts.speak, args=(text,), daemon=True).start()

	def _log_session(self) -> None:
		data = read_json(CONFIG.history_file)
		day_key = datetime.now().strftime("%Y-%m-%d")
		day = data.get(day_key, {"completed_focus_sessions": 0})
		day["completed_focus_sessions"] = int(day.get("completed_focus_sessions", 0)) + 1
		data[day_key] = day
		write_json(CONFIG.history_file, data)
		self._load_history_into_listbox()

	def _show_notification(self, title: str, message: str) -> None:
		# Show system notification and keep UI responsive
		threading.Thread(target=notify, args=(title, message), daemon=True).start()

	def _on_preset(self, _evt=None) -> None:
		name = self.preset_var.get()
		if name == "Pomodoro (25/5)":
			self.work_minutes_var.set(25); self.work_seconds_var.set(0)
			self.short_break_minutes_var.set(5); self.short_break_seconds_var.set(0)
			self.long_break_minutes_var.set(20); self.long_break_seconds_var.set(0)
		elif name == "Long Focus (50/10)":
			self.work_minutes_var.set(50); self.work_seconds_var.set(0)
			self.short_break_minutes_var.set(10); self.short_break_seconds_var.set(0)
			self.long_break_minutes_var.set(25); self.long_break_seconds_var.set(0)
		elif name == "Quick (15/3)":
			self.work_minutes_var.set(15); self.work_seconds_var.set(0)
			self.short_break_minutes_var.set(3); self.short_break_seconds_var.set(0)
			self.long_break_minutes_var.set(15); self.long_break_seconds_var.set(0)
		self._reset_timer()

	def _reset_timer(self) -> None:
		self.is_running = False
		self.is_paused = False
		self.mode = "idle"
		self.seconds_remaining = 0
		self._update_controls()
		self._update_status()


def run_app() -> None:
	app = PomodoroGUI()
	app.mainloop()


if __name__ == "__main__":
	run_app()


