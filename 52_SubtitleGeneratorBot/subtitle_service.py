from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Dict
from pathlib import Path
import time
import os
import io
import tempfile

from config import CONFIG
import requests


@dataclass
class SubtitleSegment:
	start: float
	end: float
	text: str
	Speaker: Optional[str] = None


def _format_timestamp_srt(seconds: float) -> str:
	ms = int(round(seconds * 1000))
	h = ms // 3600000
	ms %= 3600000
	m = ms // 60000
	ms %= 60000
	s = ms // 1000
	ms %= 1000
	return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _format_timestamp_vtt(seconds: float) -> str:
	ms = int(round(seconds * 1000))
	h = ms // 3600000
	ms %= 3600000
	m = ms // 60000
	ms %= 60000
	s = ms // 1000
	ms %= 1000
	return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def segments_to_srt(segments: List[SubtitleSegment]) -> str:
	lines: List[str] = []
	for i, seg in enumerate(segments, start=1):
		start = _format_timestamp_srt(seg.start)
		end = _format_timestamp_srt(seg.end)
		label = f"{seg.Speaker}: " if seg.Speaker else ""
		lines.append(str(i))
		lines.append(f"{start} --> {end}")
		lines.append(f"{label}{seg.text}")
		lines.append("")
	return "\n".join(lines).strip() + "\n"


def segments_to_vtt(segments: List[SubtitleSegment]) -> str:
	lines: List[str] = ["WEBVTT", ""]
	for seg in segments:
		start = _format_timestamp_vtt(seg.start)
		end = _format_timestamp_vtt(seg.end)
		label = f"{seg.Speaker}: " if seg.Speaker else ""
		lines.append(f"{start} --> {end}")
		lines.append(f"{label}{seg.text}")
		lines.append("")
	return "\n".join(lines).strip() + "\n"


def segments_to_txt(segments: List[SubtitleSegment]) -> str:
	lines: List[str] = []
	for seg in segments:
		label = f"{seg.Speaker}: " if seg.Speaker else ""
		lines.append(f"[{_format_timestamp_srt(seg.start)}] {label}{seg.text}")
	return "\n".join(lines) + "\n"


def _segment_plain_text(text: str) -> List[SubtitleSegment]:
	# Simple heuristic: split by sentences and assign 2.5s per sentence
	chunks: List[str] = []
	buf = []
	for ch in text.strip().split():
		buf.append(ch)
		if ch.endswith((".", "?", "!")) and len(buf) >= 6:
			chunks.append(" ".join(buf))
			buf = []
	if buf:
		chunks.append(" ".join(buf))
	segments: List[SubtitleSegment] = []
	cursor = 0.0
	for c in chunks:
		length = max(2.0, min(6.0, len(c) / 12.0))
		segments.append(SubtitleSegment(start=cursor, end=cursor + length, text=c))
		cursor += length + 0.2
	return segments


def _download_url(url: str) -> bytes:
	resp = requests.get(url, timeout=CONFIG.request_timeout_sec)
	resp.raise_for_status()
	return resp.content


def _download_youtube_audio(url: str) -> bytes:
	if not CONFIG.enable_youtube:
		raise RuntimeError("YouTube support disabled")
	from yt_dlp import YoutubeDL  # lazy import
	os.makedirs(CONFIG.tmp_dir, exist_ok=True)
	ydl_opts = {
		"format": "bestaudio/best",
		"outtmpl": os.path.join(CONFIG.tmp_dir, "%(id)s.%(ext)s"),
		"quiet": True,
		"no_warnings": True,
		"postprocessors": [
			{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
		],
	}
	with YoutubeDL(ydl_opts) as ydl:
		info = ydl.extract_info(url, download=True)
		aid = info.get("id")
		# Postprocessor emits mp3
		candidate = os.path.join(CONFIG.tmp_dir, f"{aid}.mp3")
		if not os.path.exists(candidate):
			# fallback to original file if mp3 not produced
			ext = info.get("ext", "mp4")
			candidate = os.path.join(CONFIG.tmp_dir, f"{aid}.{ext}")
		with open(candidate, "rb") as f:
			return f.read()


class SubtitleService:
	def __init__(self) -> None:
		self._real = CONFIG.use_real_transcription and bool(CONFIG.openai_api_key)

	def is_enabled(self) -> bool:
		return True

	def fetch_media_bytes(self, media_url: str) -> bytes:
		if ("youtube.com" in media_url or "youtu.be" in media_url):
			return _download_youtube_audio(media_url)
		return _download_url(media_url)

	def transcribe(self, media_bytes: bytes, source_lang: str = "en", auto_sync: bool = True, speaker_labels: bool = False) -> List[SubtitleSegment]:
		if self._real:
			try:
				files = {"file": ("audio.wav", media_bytes)}
				data = {"model": CONFIG.openai_model, "response_format": "text", "language": source_lang}
				headers = {"Authorization": f"Bearer {CONFIG.openai_api_key}"}
				resp = requests.post("https://api.openai.com/v1/audio/transcriptions", headers=headers, data=data, files=files, timeout=CONFIG.request_timeout_sec)
				resp.raise_for_status()
				text = resp.text.strip()
				return _segment_plain_text(text or "")
			except Exception:
				pass
		text = "This is a sample transcription. Replace with real API call."
		return _segment_plain_text(text)

	def format(self, segments: List[SubtitleSegment], fmt: str = "srt") -> str:
		fmt = (fmt or "srt").lower()
		if fmt == "srt":
			return segments_to_srt(segments)
		if fmt == "vtt":
			return segments_to_vtt(segments)
		return segments_to_txt(segments)

	def save_outputs(self, slug: str, base_name: str, segments: List[SubtitleSegment]) -> Dict[str, str]:
		out_dir = Path(CONFIG.subtitles_dir) / slug
		out_dir.mkdir(parents=True, exist_ok=True)
		paths: Dict[str, str] = {}
		for ext in ("srt", "vtt", "txt"):
			content = self.format(segments, ext)
			p = out_dir / f"{base_name}.{ext}"
			p.write_text(content, encoding="utf-8")
			paths[ext] = str(p)
		return paths


def slugify(name: str) -> str:
	import re
	value = (name or "media").strip().lower()
	value = re.sub(r"[^a-z0-9\-\s]", "", value)
	value = re.sub(r"\s+", "-", value)
	return value or "media"
