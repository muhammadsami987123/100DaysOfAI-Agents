from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from pathlib import Path

from backend.agent import DailyMotivationAgent
from backend.tts import TTSService
from backend.config import Config

# Get the base directory for relative paths
BASE_DIR = Path(__file__).parent.parent

# Initialize FastAPI app
app = FastAPI()

# Configure static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
templates = Jinja2Templates(directory="frontend")

# Initialize services
motivation_agent = DailyMotivationAgent()
tts_service = TTSService()

class GenerateRequest(BaseModel):
    name: str | None = None
    language: str = "en"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_motivation_endpoint(request_body: GenerateRequest):
    try:
        motivation_data = motivation_agent.generate_motivation(name=request_body.name)
        full_text = f"{motivation_data['quote']}. {motivation_data['message']}"
        audio_url = tts_service.generate_audio(text=full_text, lang=request_body.language)

        return {
            "quote": motivation_data['quote'],
            "message": motivation_data['message'],
            "audio_url": audio_url
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")

@app.get("/api/about", response_class=HTMLResponse)
async def get_about_content():
    try:
        with open(BASE_DIR / "README.md", "r", encoding="utf-8") as f:
            readme_content = f.read()
        return readme_content
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="README.md not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading README.md: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
