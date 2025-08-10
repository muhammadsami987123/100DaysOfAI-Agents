from __future__ import annotations

import io
import os
from typing import Optional

import httpx
from fastapi import FastAPI, Form, File, UploadFile, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import PORT, MAX_CHARACTERS
from tts_service import synthesize_speech, TextToSpeechError, SUPPORTED_LANGUAGES

try:
    import trafilatura
except Exception:  # noqa: BLE001
    trafilatura = None


app = FastAPI(title="TextToSpeechAgent")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
static_dir = os.path.join(BASE_DIR, "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "languages": SUPPORTED_LANGUAGES,
        },
    )


@app.post("/api/tts")
async def tts_endpoint(
    text: Optional[str] = Form(default=None),
    language: str = Form(default="auto"),
    gender: str = Form(default="female"),
    file: Optional[UploadFile] = File(default=None),
    url: Optional[str] = Form(default=None),
):
    try:
        # Log the received parameters for debugging
        print(f"Received TTS request - text: {text}, language: {language}, gender: {gender}, file: {file.filename if file else None}, url: {url}")
        
        input_text = await _resolve_input_text(text=text, file=file, url=url)
        print(f"Resolved input text length: {len(input_text)}")
        
        audio_bytes = synthesize_speech(
            input_text,
            language=language,
            gender=gender,
            max_chars=MAX_CHARACTERS,
        )
        print(f"Generated audio bytes length: {len(audio_bytes)}")
        
        filename = "speech.mp3"
        headers = {"Content-Disposition": f"attachment; filename={filename}"}
        return StreamingResponse(io.BytesIO(audio_bytes), media_type="audio/mpeg", headers=headers)
    except TextToSpeechError as e:
        print(f"TTS Error: {e}")
        return JSONResponse({"error": str(e)}, status_code=400)
    except Exception as e:  # noqa: BLE001
        print(f"Server Error: {e}")
        return JSONResponse({"error": f"Server error: {e}"}, status_code=500)


async def _resolve_input_text(
    text: Optional[str],
    file: Optional[UploadFile],
    url: Optional[str],
) -> str:
    print(f"Resolving input - text: {text}, file: {file.filename if file else None}, url: {url}")
    
    if text and text.strip():
        print(f"Using text input: {text[:100]}...")
        return text.strip()

    if file and file.filename:
        print(f"Using file input: {file.filename}")
        content = await file.read()
        try:
            decoded_content = content.decode("utf-8").strip()
            print(f"File content length: {len(decoded_content)}")
            return decoded_content
        except UnicodeDecodeError:
            decoded_content = content.decode("latin-1", errors="ignore").strip()
            print(f"File content length (latin-1): {len(decoded_content)}")
            return decoded_content

    if url and url.strip():
        print(f"Using URL input: {url}")
        extracted = await _extract_text_from_url(url.strip())
        if extracted:
            print(f"URL content length: {len(extracted)}")
            return extracted
        raise TextToSpeechError("Could not extract text from the provided URL.")

    raise TextToSpeechError("No input provided. Please provide Text, File, or URL.")


async def _extract_text_from_url(page_url: str) -> Optional[str]:
    if trafilatura is None:
        # Fallback: simple HTTP GET and naive extraction
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(page_url, follow_redirects=True)
            resp.raise_for_status()
            text = resp.text
            return text if text else None

    downloaded = trafilatura.fetch_url(page_url)
    if not downloaded:
        return None
    extracted = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
    if extracted:
        return extracted.strip()
    return None


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=PORT, reload=False)


