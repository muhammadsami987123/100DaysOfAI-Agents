from __future__ import annotations

"""
Optional voice input and speech output utilities.
Kept minimal and disabled by default via config.
"""

from typing import Optional


def transcribe_from_mic(language: str = "en-US") -> Optional[str]:
    try:
        import speech_recognition as sr
    except Exception:
        return None

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, phrase_time_limit=20)
    try:
        return recognizer.recognize_google(audio, language=language)
    except Exception:
        return None


def speak(text: str, rate: int = 170) -> bool:
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", rate)
        engine.say(text)
        engine.runAndWait()
        return True
    except Exception:
        return False


