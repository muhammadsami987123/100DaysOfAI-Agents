from __future__ import annotations

from typing import Optional


class Notifier:
    def __init__(self) -> None:
        self._toast = None
        try:
            from win10toast import ToastNotifier  # type: ignore
            self._toast = ToastNotifier()
        except Exception:
            self._toast = None

    def toast(self, message: str, title: str = "TextFixer", duration_ms: int = 800) -> None:
        # Only available on Windows with win10toast installed; otherwise no-op
        if not self._toast:
            return
        # win10toast expects seconds
        duration_s = max(0, int(round(duration_ms / 1000))) or 1
        try:
            self._toast.show_toast(title, message, duration=duration_s, threaded=True)
        except Exception:
            pass


