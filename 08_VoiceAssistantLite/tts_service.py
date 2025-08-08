from __future__ import annotations

import pyttsx3

from config import CONFIG


class TTSService:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        # Apply rate if provided
        try:
            self.engine.setProperty("rate", int(CONFIG.tts_rate))
        except Exception:
            pass

    def speak(self, text: str) -> None:
        if not text:
            return
        self.engine.say(text)
        self.engine.runAndWait()


