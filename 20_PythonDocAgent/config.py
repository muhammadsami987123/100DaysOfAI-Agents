"""
Configuration and utilities for PythonDocAgent (Day 20).

- Loads environment from .env if present
- Provides typed accessors with sane defaults
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict

from dotenv import load_dotenv


load_dotenv(override=False)


SUPPORTED_LANGUAGES: Dict[str, Dict[str, str]] = {
    "en": {
        "name": "English",
        "explain": "Explaining the code/documentation in clear, professional English...",
        "summarize": "Summarizing the content section-wise in English...",
        "walkthrough": "Starting line-by-line walkthrough in English...",
        "complete": "Completed.",
        "streaming": "Streaming response...",
        "saving": "Saving output...",
        "saved": "Saved.",
        "fetching": "Fetching and parsing content...",
        "analyzing": "Analyzing with OpenAI...",
        "copied": "Code copied to clipboard.",
    },
    "hi": {
        "name": "Hindi",
        "explain": "कोड/डॉक्यूमेंट को सरल हिंदी में समझाया जा रहा है...",
        "summarize": "हिंदी में सेक्शन-वाइज़ सारांश बनाया जा रहा है...",
        "walkthrough": "लाइन-बाई-लाइन वॉकथ्रू शुरू...",
        "complete": "समाप्त।",
        "streaming": "स्ट्रीमिंग प्रतिक्रिया...",
        "saving": "आउटपुट सेव हो रहा है...",
        "saved": "सेव हो गया।",
        "fetching": "कंटेंट प्राप्त और पार्स किया जा रहा है...",
        "analyzing": "OpenAI के साथ विश्लेषण...",
        "copied": "कोड क्लिपबोर्ड में कॉपी हो गया।",
    },
    "ur": {
        "name": "Urdu",
        "explain": "کوڈ/دستاویزات کی سادہ اردو میں وضاحت کی جا رہی ہے...",
        "summarize": "اردو میں سیکشن وار خلاصہ تیار کیا جا رہا ہے...",
        "walkthrough": "لائن بہ لائن وضاحت شروع...",
        "complete": "مکمل۔",
        "streaming": "جواب نشر کیا جا رہا ہے...",
        "saving": "آؤٹ پٹ محفوظ کیا جا رہا ہے...",
        "saved": "محفوظ ہوگیا۔",
        "fetching": "مواد لایا اور پارس کیا جا رہا ہے...",
        "analyzing": "OpenAI کے ساتھ تجزیہ...",
        "copied": "کوڈ کلپ بورڈ میں کاپی ہو گیا۔",
    },
}


def get_language_config(code: str) -> Dict[str, str]:
    code = (code or "en").lower()
    return SUPPORTED_LANGUAGES.get(code, SUPPORTED_LANGUAGES["en"]) 


@dataclass
class Settings:
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    temperature: float = 0.2
    max_tokens: int = 1200
    stream: bool = True
    history_max_turns: int = 100
    voice_input_enabled: bool = False
    tts_enabled: bool = False
    default_language: str = "en"


def load_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=float(os.getenv("TEMPERATURE", "0.2")),
        max_tokens=int(os.getenv("MAX_TOKENS", "1200")),
        stream=os.getenv("STREAM", "true").lower() == "true",
        history_max_turns=int(os.getenv("HISTORY_MAX_TURNS", "100")),
        voice_input_enabled=os.getenv("VOICE_INPUT", "false").lower() == "true",
        tts_enabled=os.getenv("SPEECH_OUTPUT", "false").lower() == "true",
        default_language=os.getenv("LANGUAGE", "en"),
    )


def validate_config() -> list[str]:
    errors: list[str] = []
    settings = load_settings()
    if not settings.openai_api_key:
        errors.append("OPENAI_API_KEY is required. Create a .env file or set the environment variable.")
    if settings.default_language.lower() not in SUPPORTED_LANGUAGES:
        errors.append(f"LANGUAGE must be one of: {', '.join(SUPPORTED_LANGUAGES.keys())}")
    return errors


