from __future__ import annotations

import io
from typing import Optional, Tuple

import speech_recognition as sr

from config import CONFIG


class STTService:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()

    def listen(self, timeout: Optional[float] = None, phrase_time_limit: Optional[float] = None) -> sr.AudioData:
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
            audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        return audio

    def transcribe(self, audio: sr.AudioData) -> Tuple[str, str]:
        provider = CONFIG.stt_provider
        language = CONFIG.language
        if provider == "whisper_local":
            text, used_language = self._transcribe_whisper_local(audio)
        else:
            text, used_language = self._transcribe_google(audio, language)
        return text, used_language

    def _transcribe_google(self, audio: sr.AudioData, language: str) -> Tuple[str, str]:
        try:
            text = self.recognizer.recognize_google(audio, language=language)
            return text, language
        except sr.UnknownValueError:
            return "", language
        except sr.RequestError:
            # Fallback to no result; caller can handle
            return "", language

    def _transcribe_whisper_local(self, audio: sr.AudioData) -> Tuple[str, str]:
        try:
            import whisper  # type: ignore
        except Exception:
            return "", CONFIG.language

        wav_bytes = audio.get_wav_data()
        audio_buffer = io.BytesIO(wav_bytes)

        # Save to temporary in-memory file for whisper
        # whisper.load_audio can take bytes path via ffmpeg; we use BytesIO+temp file fallback
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_buffer.read())
            tmp_path = tmp.name

        try:
            model = whisper.load_model(CONFIG.whisper_model, device=CONFIG.whisper_device)
            options = {"task": "transcribe"}
            if CONFIG.language and CONFIG.language.lower() != "auto":
                options["language"] = CONFIG.language
            result = model.transcribe(tmp_path, **options)
            text = (result or {}).get("text", "").strip()
            detected_lang = (result or {}).get("language", CONFIG.language)
            return text, detected_lang
        except Exception:
            return "", CONFIG.language
        finally:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass


