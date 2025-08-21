from __future__ import annotations

import threading
import time
from typing import Callable, Optional

import pyperclip
from pynput import keyboard

from config import CONFIG
from notifier import Notifier


def _send_keys(controller: keyboard.Controller, keys: list) -> None:
    for key in keys:
        controller.press(key)
    for key in reversed(keys):
        controller.release(key)


def _copy_selection(controller: keyboard.Controller) -> Optional[str]:
    try:
        previous_clipboard = pyperclip.paste()
    except Exception:
        previous_clipboard = None

    # Ctrl+C to copy
    _send_keys(controller, [keyboard.Key.ctrl, keyboard.KeyCode.from_char('c')])
    time.sleep(CONFIG.copy_wait_ms / 1000.0)

    try:
        copied = pyperclip.paste()
    except Exception:
        copied = None

    # Basic sanity check: if clipboard unchanged, we still proceed
    return copied


def _paste_text(controller: keyboard.Controller, text: str) -> None:
    pyperclip.copy(text)
    time.sleep(0.05)
    _send_keys(controller, [keyboard.Key.ctrl, keyboard.KeyCode.from_char('v')])
    time.sleep(CONFIG.paste_wait_ms / 1000.0)


class TextFixerHotkey:
    def __init__(self, on_text: Callable[[str], str], on_undo: Optional[Callable[[], None]] = None) -> None:
        self._on_text = on_text
        self._on_undo = on_undo
        self._controller = keyboard.Controller()
        self._listener: Optional[keyboard.GlobalHotKeys] = None
        self._last_original: Optional[str] = None
        self._last_corrected: Optional[str] = None
        self._notifier = Notifier()

    def _do_fix(self) -> None:
        # run in background thread to avoid blocking UI
        try:
            original_clipboard = pyperclip.paste() if CONFIG.restore_clipboard else None
        except Exception:
            original_clipboard = None

        text = _copy_selection(self._controller) or ""
        if not text.strip():
            return
        self._last_original = text
        try:
            corrected = self._on_text(text)
        except Exception:
            return
        if corrected and corrected != text:
            self._last_corrected = corrected
            _paste_text(self._controller, corrected)
            if CONFIG.restore_clipboard and original_clipboard is not None:
                try:
                    pyperclip.copy(original_clipboard)
                except Exception:
                    pass
            if CONFIG.toast_enabled:
                self._notifier.toast("Corrected", duration_ms=CONFIG.toast_duration_ms)

    def _handle_fix(self) -> None:
        threading.Thread(target=self._do_fix, daemon=True).start()

    def _handle_undo(self) -> None:
        if self._last_original and self._last_corrected:
            # Select previous text via Ctrl+Z if available; otherwise paste original over selection
            # Attempt Ctrl+Z first
            _send_keys(self._controller, [keyboard.Key.ctrl, keyboard.KeyCode.from_char('z')])
            time.sleep(0.05)
            if self._on_undo:
                try:
                    self._on_undo()
                except Exception:
                    pass

    def start(self) -> None:
        hotkey = CONFIG.hotkey
        undo_hotkey = CONFIG.undo_hotkey
        self._listener = keyboard.GlobalHotKeys({
            hotkey: self._handle_fix,
            undo_hotkey: self._handle_undo,
        })
        self._listener.start()

    def join(self) -> None:
        if self._listener:
            self._listener.join()


