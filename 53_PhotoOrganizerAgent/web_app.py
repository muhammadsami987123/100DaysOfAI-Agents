from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from core.organizer import PhotoOrganizer

app = FastAPI(title="PhotoOrganizerAgent Web UI")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/organize", response_class=HTMLResponse)
async def organize(request: Request, folder: str = Form(...), mode: str = Form(...)):
    organizer = PhotoOrganizer(mode)
    moved = []
    try:
        for filename in os.listdir(folder):
            if any(filename.lower().endswith(ext) for ext in organizer.CONFIG.PHOTO_EXTENSIONS):
                photo_path = os.path.join(folder, filename)
                detected = organizer.mock_detect(photo_path)
                target_folder = os.path.join(folder, detected)
                os.makedirs(target_folder, exist_ok=True)
                new_path = os.path.join(target_folder, filename)
                os.rename(photo_path, new_path)
                moved.append(f"Moved {filename} to {detected}/")
        result = f"Organized {len(moved)} photo(s).<br>" + '<br>'.join(moved)
    except Exception as e:
        result = f"Error: {e}"
    return templates.TemplateResponse("index.html", {"request": request, "result": result})

# Entrypoint for uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8053)
