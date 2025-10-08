from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pathlib import Path
import uvicorn

from config import Config
from math_agent import MathSolverAgent

BASE_DIR = Path(__file__).parent
# TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static" / "assets"

# Ensure directories exist
STATIC_DIR.mkdir(parents=True, exist_ok=True)
# TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

# templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

app = FastAPI(title="MathSolverAgent", description="AI agent that solves math equations step-by-step", version="1.0.0")
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

class SolveRequest(BaseModel):
    problem: str

agent: MathSolverAgent = None
try:
    agent = MathSolverAgent()
except Exception as e:
    print(f"Warning: MathSolverAgent init failed: {e}")
    Config.validate() # Call validate here too for initial checks

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # return templates.TemplateResponse("index.html", {"request": request})
    with open(STATIC_DIR / "index.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/solve")
async def solve_problem_get():
    return {"message": "This is the GET endpoint for /api/solve. Use POST to submit problems."}

@app.post("/api/solve")
async def solve_problem_api(payload: SolveRequest):
    if agent is None:
        raise HTTPException(status_code=500, detail="MathSolverAgent not initialized.")
    try:
        solution = agent.solve_math_problem(payload.problem)
        return solution
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host=Config.HOST, port=Config.PORT, reload=Config.DEBUG)
