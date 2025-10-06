from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
import uvicorn

from config import Config
from news_agent import VoiceNewsAgent


BASE_DIR = Path(__file__).parent

# Ensure required directories exist before mounting
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
AUDIO_DIR = BASE_DIR / Config.AUDIO_DIR
STATIC_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

app = FastAPI(title=Config.APP_TITLE, description=Config.APP_DESCRIPTION, version="1.0.0")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/audio", StaticFiles(directory=str(AUDIO_DIR)), name="audio")


class ReadRequest(BaseModel):
    category: Optional[str] = None
    country: Optional[str] = None
    q: Optional[str] = None
    limit: int = 5
    language: Optional[str] = "en"
    date_range: Optional[str] = "any"  # any|day|week|month
    voice_gender: Optional[str] = "female"
    voice_rate: Optional[int] = None
    voice_pitch: Optional[float] = None
    transcript: bool = True


agent: Optional[VoiceNewsAgent] = None
try:
    Config.validate()
    agent = VoiceNewsAgent()
except Exception as e:
    print(f"Warning: Agent init failed: {e}")
    agent = None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/read")
async def read_news(payload: ReadRequest):
    if agent is None:
        raise HTTPException(status_code=500, detail="Agent not available")
    try:
        result = agent.read_news(
            category=payload.category,
            country=payload.country,
            q=payload.q,
            limit=payload.limit,
            language=payload.language,
            date_range=payload.date_range,
            voice_gender=payload.voice_gender,
            voice_rate=payload.voice_rate,
            voice_pitch=payload.voice_pitch,
            transcript=payload.transcript,
        )
        if not result.get("success"):
            return JSONResponse(result, status_code=400)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "agent_available": agent is not None,
        "tts_engine": Config.TTS_ENGINE,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host=Config.HOST, port=Config.PORT, reload=Config.DEBUG)


