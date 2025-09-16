from __future__ import annotations

import os
from typing import Optional, List

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import CONFIG
from vision_service import VisionCaptioner


app = FastAPI(title="ImageCaptionBot")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
static_dir = os.path.join(BASE_DIR, "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


SUPPORTED_LANGUAGES = [
    {"code": "en", "name": "English"},
    {"code": "ur", "name": "Urdu"},
    {"code": "hi", "name": "Hindi"},
]

STYLES = [
    {"code": "descriptive", "name": "Descriptive"},
    {"code": "creative", "name": "Creative"},
    {"code": "alt", "name": "Alt-text"},
]

LENGTHS = [
    {"code": "short", "name": "Short"},
    {"code": "medium", "name": "Medium"},
    {"code": "long", "name": "Long"},
]


def _guess_mime(filename: str) -> str:
    low = filename.lower()
    if low.endswith((".jpg", ".jpeg")):
        return "image/jpeg"
    if low.endswith(".png"):
        return "image/png"
    if low.endswith(".webp"):
        return "image/webp"
    return "application/octet-stream"


@app.on_event("startup")
async def startup_event() -> None:
    if not CONFIG.openai_api_key:
        # still allow UI to load; API will return 500 until key set
        print("Warning: OPENAI_API_KEY not set. /api/caption will fail until configured.")
    else:
        print("OPENAI_API_KEY successfully loaded.")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "languages": SUPPORTED_LANGUAGES, "styles": STYLES, "lengths": LENGTHS},
    )


@app.post("/api/caption")
async def caption_endpoint(
    image: UploadFile = File(...),
    language: str = Form(default="en"),
    style: str = Form(default="descriptive"),
    length: str = Form(default="short"),
    hashtags: int = Form(default=0),
):
    try:
        ext_ok = any(image.filename.lower().endswith(ext) for ext in CONFIG.allowed_exts)
        if not ext_ok:
            raise HTTPException(status_code=400, detail="Unsupported file type. Use jpg/png/webp.")

        data = await image.read()
        if not data:
            raise HTTPException(status_code=400, detail="Empty file upload")
        if len(data) > CONFIG.max_image_bytes:
            raise HTTPException(status_code=400, detail="Image exceeds max size limit (8MB)")

        if not CONFIG.openai_api_key:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")

        captioner = VisionCaptioner(CONFIG.openai_api_key, CONFIG.openai_model)
        mime = _guess_mime(image.filename)
        caption = captioner.generate_caption(
            data,
            mime,
            language=language,
            style=style,
            length=length,
            hashtags=bool(int(hashtags)),
        )
        if not caption:
            raise HTTPException(status_code=500, detail="Failed to generate caption")

        return {"success": True, "caption": caption, "language": language, "style": style, "length": length, "hashtags": bool(int(hashtags))}
    except HTTPException as he:
        raise he
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.post("/api/captions/batch")
async def captions_batch_endpoint(
    images: List[UploadFile] = File(...),
    language: str = Form(default="en"),
    tone: str = Form(default="professional"),
    variations: int = Form(default=10),
    temperature: float = Form(default=0.95),
):
    try:
        if not CONFIG.openai_api_key:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")

        captioner = VisionCaptioner(CONFIG.openai_api_key, CONFIG.openai_model)
        all_captions = []
        for img in images:
            ext_ok = any(img.filename.lower().endswith(ext) for ext in CONFIG.allowed_exts)
            if not ext_ok:
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {img.filename}")
            data = await img.read()
            if not data:
                raise HTTPException(status_code=400, detail=f"Empty file: {img.filename}")
            if len(data) > CONFIG.max_image_bytes:
                raise HTTPException(status_code=400, detail=f"Image too large: {img.filename}")

            mime = _guess_mime(img.filename)
            platform_map = captioner.generate_platform_captions(
                data, mime, language=language, tone=tone, variations=int(variations), temperature=float(temperature)
            )
            for platform, captions_list in platform_map.items():
                for caption_data in captions_list:
                    all_captions.append({
                        "platform": platform,
                        "title": img.filename, # Using filename as title as per instruction
                        "caption": caption_data.get("caption", ""),
                        "hashtags": caption_data.get("hashtags", []),
                    })

        return all_captions # Return the flattened list of captions directly
    except HTTPException as he:
        raise he
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host=CONFIG.host, port=CONFIG.port, reload=CONFIG.debug)


