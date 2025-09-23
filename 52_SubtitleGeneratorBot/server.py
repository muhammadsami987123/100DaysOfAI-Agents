from __future__ import annotations

from typing import Dict, Any, Optional
from pathlib import Path
import os

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import CONFIG
from subtitle_service import SubtitleService, slugify


BASE_DIR = Path(__file__).parent.resolve()
TEMPLATES_DIR = Path(CONFIG.templates_dir)
STATIC_DIR = Path(CONFIG.static_dir)
SUBTITLES_DIR = Path(CONFIG.subtitles_dir)


def create_app() -> FastAPI:
	app = FastAPI(title="SubtitleGeneratorBot")

	# Ensure directories exist
	STATIC_DIR.mkdir(parents=True, exist_ok=True)
	TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
	SUBTITLES_DIR.mkdir(parents=True, exist_ok=True)
	Path(CONFIG.tmp_dir).mkdir(parents=True, exist_ok=True)

	templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
	app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
	app.mount("/subtitles", StaticFiles(directory=str(SUBTITLES_DIR)), name="subtitles")

	service = SubtitleService()

	@app.get("/", response_class=HTMLResponse)
	async def home(request: Request) -> HTMLResponse:
		return templates.TemplateResponse(
			"index.html",
			{
				"request": request,
				"languages": [
					{"code": "en", "label": "English"},
					{"code": "ur", "label": "Urdu"},
					{"code": "hi", "label": "Hindi"},
				],
			}
		)

	@app.post("/api/process")
	async def process(
		request: Request,
		file: Optional[UploadFile] = File(default=None),
		media_url: Optional[str] = Form(default=None),
		source_lang: str = Form(default="en"),
		fmt: str = Form(default="srt"),
		auto_sync: bool = Form(default=True),
		speaker_labels: bool = Form(default=False),
		translate: Optional[str] = Form(default=None),
	):
		media_bytes: Optional[bytes] = None
		name_hint = "uploaded-media"
		if file is not None:
			media_bytes = await file.read()
			name_hint = file.filename or name_hint
		elif media_url:
			try:
				media_bytes = service.fetch_media_bytes(media_url)
				name_hint = Path(media_url).stem or name_hint
			except Exception as e:
				return JSONResponse({"success": False, "error": f"Failed to fetch URL: {e}"}, status_code=400)
		else:
			return JSONResponse({"success": False, "error": "Provide a file or a media_url"}, status_code=400)

		segments = service.transcribe(media_bytes, source_lang=source_lang, auto_sync=auto_sync, speaker_labels=speaker_labels)
		slug = slugify(name_hint)
		paths = service.save_outputs(slug, base_name=slug, segments=segments)

		preview = {
			"srt": f"/subtitles/{slug}/{slug}.srt",
			"vtt": f"/subtitles/{slug}/{slug}.vtt",
			"txt": f"/subtitles/{slug}/{slug}.txt",
		}

		return JSONResponse({
			"success": True,
			"slug": slug,
			"download": preview,
			"fmt": fmt,
			"real": CONFIG.use_real_transcription,
			"youtube": CONFIG.enable_youtube,
		})

	@app.get("/download/{slug}/{filename}")
	async def download(slug: str, filename: str):
		path = SUBTITLES_DIR / slug / filename
		if not path.exists():
			return JSONResponse({"success": False, "error": "File not found"}, status_code=404)
		media_type = "text/plain"
		if filename.endswith(".srt"):
			media_type = "application/x-subrip"
		elif filename.endswith(".vtt"):
			media_type = "text/vtt"
		return FileResponse(str(path), filename=filename, media_type=media_type)

	return app
