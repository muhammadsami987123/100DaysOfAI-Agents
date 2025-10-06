import os
import tempfile
import base64
from typing import Optional, Tuple

from config import Config

# Optional deps
try:
    import google.generativeai as genai  # Gemini
except Exception:
    genai = None  # type: ignore

try:
    from gtts import gTTS
except Exception:
    gTTS = None  # type: ignore

try:
    import pyttsx3
except Exception:
    pyttsx3 = None  # type: ignore


class TTSService:
    """TTS with Gemini preference and fallbacks (gTTS, pyttsx3)."""

    def __init__(self) -> None:
        self.engine = Config.TTS_ENGINE
        self.language = Config.TTS_LANGUAGE
        self.default_gender = Config.TTS_DEFAULT_GENDER
        self.rate = Config.TTS_RATE
        self.pitch = Config.TTS_PITCH
        self.max_chars = Config.MAX_TTS_CHARS

        self.gemini_ready = False
        if self.engine == "gemini" and genai and Config.GEMINI_API_KEY:
            try:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_ready = True
            except Exception:
                self.gemini_ready = False

        self.pyttsx3_engine = None
        if pyttsx3:
            try:
                self.pyttsx3_engine = pyttsx3.init()
                self.pyttsx3_engine.setProperty("rate", self.rate)
            except Exception:
                self.pyttsx3_engine = None

        os.makedirs(Config.AUDIO_DIR, exist_ok=True)

    def synthesize(self, text: str, *, gender: Optional[str] = None, rate: Optional[int] = None, pitch: Optional[float] = None) -> Tuple[str, bytes]:
        text = (text or "").strip()
        if not text:
            raise ValueError("Empty text for TTS")
        if len(text) > self.max_chars:
            text = text[: self.max_chars]

        voice_gender = (gender or self.default_gender).lower()
        voice_rate = rate or self.rate
        voice_pitch = pitch or self.pitch

        audio_bytes: Optional[bytes] = None
        mime = "audio/mpeg"

        # Prefer Gemini
        if self.gemini_ready:
            try:
                # Gemini TTS experimental: use Audio generation if available; fallback to text->audio via model instruction
                model_name = Config.GEMINI_TTS_MODEL
                model = genai.GenerativeModel(model_name)
                prompt = f"Read the following news in a natural {voice_gender} voice, speaking clearly. Keep pace ~{voice_rate} wpm, pitch factor {voice_pitch}. Text:\n\n{text}"
                resp = model.generate_content(prompt, generation_config={"response_mime_type": "audio/mpeg"})
                if hasattr(resp, "candidates") and resp.candidates:
                    part = resp.candidates[0].content.parts[0]
                    # SDK returns inline bytes for audio if supported
                    if hasattr(part, "inline_data") and getattr(part.inline_data, "data", None):
                        audio_bytes = base64.b64decode(part.inline_data.data)
                if audio_bytes:
                    return mime, audio_bytes
            except Exception:
                pass

        # gTTS fallback
        if gTTS:
            try:
                tts = gTTS(text=text, lang=(self.language or "en"), slow=False)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    temp_path = f.name
                tts.save(temp_path)
                with open(temp_path, "rb") as f:
                    audio_bytes = f.read()
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass
                if audio_bytes:
                    return mime, audio_bytes
            except Exception:
                pass

        # pyttsx3 fallback (returns WAV)
        if self.pyttsx3_engine:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                    temp_path = f.name
                self.pyttsx3_engine.save_to_file(text, temp_path)
                self.pyttsx3_engine.runAndWait()
                with open(temp_path, "rb") as f:
                    audio_bytes = f.read()
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass
                if audio_bytes:
                    return "audio/wav", audio_bytes
            except Exception:
                pass

        raise RuntimeError("No TTS engine available")


