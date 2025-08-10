from __future__ import annotations

import io
from typing import Optional

from gtts import gTTS
from openai import OpenAI

from config import OPENAI_API_KEY, TTS_ENGINE, DEFAULT_VOICE_FEMALE, DEFAULT_VOICE_MALE


SUPPORTED_LANGUAGES = {
    "auto": None,
    "en": "English",
    "hi": "Hindi",
    "ur": "Urdu",
}


class TextToSpeechError(Exception):
    pass


def _sanitize_text(text: str, max_chars: int) -> str:
    text = (text or "").strip()
    if not text:
        raise TextToSpeechError("Empty text provided.")
    if len(text) > max_chars:
        text = text[:max_chars]
    return text


def synthesize_speech(
    text: str,
    language: str = "auto",
    gender: str = "female",
    max_chars: int = 8000,
) -> bytes:
    text = _sanitize_text(text, max_chars)

    # Prefer OpenAI if configured; else gTTS
    if TTS_ENGINE == "openai" and OPENAI_API_KEY:
        return _synthesize_openai(text, language=language, gender=gender)
    return _synthesize_gtts(text, language=language)


def _synthesize_gtts(text: str, language: str = "auto") -> bytes:
    # gTTS supports language autodetection via langdetect? Not directly; we fall back to en if auto
    lang_code = language if language in ("en", "hi", "ur") else "en"
    fp = io.BytesIO()
    tts = gTTS(text=text, lang=lang_code)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()


def _synthesize_openai(text: str, language: str = "auto", gender: str = "female") -> bytes:
    client = OpenAI(api_key=OPENAI_API_KEY)

    # The OpenAI TTS API does not require language code explicitly; we can prepend a brief instruction
    # to encourage correct pronunciation for non-English text.
    voice = DEFAULT_VOICE_FEMALE if gender.lower() == "female" else DEFAULT_VOICE_MALE

    # Use the correct TTS model names
    model_candidates = ["tts-1", "tts-1-hd"]

    last_error: Optional[Exception] = None
    for model_name in model_candidates:
        try:
            print(f"Trying OpenAI TTS with model: {model_name}, voice: {voice}")
            audio = client.audio.speech.create(
                model=model_name,
                voice=voice,
                input=text,
            )
            print(f"Successfully created audio with model: {model_name}")
            return audio.read()
        except Exception as e:  # noqa: BLE001
            print(f"Failed with model {model_name}: {e}")
            last_error = e
            continue

    raise TextToSpeechError(f"OpenAI TTS failed: {last_error}")


