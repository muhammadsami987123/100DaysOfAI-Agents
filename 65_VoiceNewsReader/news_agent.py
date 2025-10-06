from typing import Dict, Any, List, Optional, Tuple
from config import Config
from news_service import NewsService
from tts_service import TTSService


class VoiceNewsAgent:
    """Orchestrates fetching headlines, summarizing, and synthesizing audio."""

    def __init__(self) -> None:
        self.news = NewsService()
        self.tts = TTSService()

    def read_news(
        self,
        *,
        category: Optional[str],
        country: Optional[str],
        q: Optional[str],
        limit: int,
        language: Optional[str],
        date_range: Optional[str],
        voice_gender: Optional[str],
        voice_rate: Optional[int],
        voice_pitch: Optional[float],
        transcript: bool = True,
    ) -> Dict[str, Any]:
        items = self.news.fetch_top_headlines(
            category=category or Config.DEFAULT_CATEGORY,
            country=country or Config.DEFAULT_COUNTRY,
            q=q,
            limit=limit or Config.DEFAULT_LIMIT,
            language=language or Config.TTS_LANGUAGE,
            date_range=date_range or "any",
        )

        if not items:
            return {"success": False, "error": "No news available. Check API keys or filters."}

        # Build script: title + short summary lines
        lines: List[str] = []
        for idx, it in enumerate(items[:limit]):
            title = (it.get("title") or "").strip()
            desc = (it.get("description") or "").strip()
            source = (it.get("source") or "").strip()
            line = f"{idx+1}. {title} — {source}. {desc}"
            lines.append(line)
        script = "\n".join(lines)

        # TTS language handling: pass through language for engines that support it
        if hasattr(self.tts, "language"):
            self.tts.language = (language or Config.TTS_LANGUAGE) or "en"

        mime, audio_bytes = self.tts.synthesize(
            script,
            gender=voice_gender,
            rate=voice_rate,
            pitch=voice_pitch,
        )

        # Persist audio to file for download
        ext = ".mp3" if mime == "audio/mpeg" else ".wav"
        filename = f"news_{abs(hash(script))}{ext}"
        path = f"{Config.AUDIO_DIR}/{filename}"
        with open(path, "wb") as f:
            f.write(audio_bytes)

        payload: Dict[str, Any] = {
            "success": True,
            "items": items[:limit],
            "audio_mime": mime,
            "audio_filename": filename,
            "audio_url": f"/audio/{filename}",
        }
        if transcript:
            payload["transcript"] = script
        return payload


