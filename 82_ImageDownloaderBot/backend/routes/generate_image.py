from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..utils.gemini_helper import generate_image_gemini
from ..utils.openai_helper import generate_image_openai
from ..utils.file_handler import save_generated_image
import traceback

router = APIRouter()

class GenerateImageRequest(BaseModel):
    prompt: str
    model: str = "gemini"  # 'gemini' or 'openai'

@router.post("/generate")
async def generate_image(request: GenerateImageRequest):
    try:
        # Input validation
        if not request.prompt or len(request.prompt.strip()) == 0:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")

        if request.model not in ["gemini", "openai"]:
            raise HTTPException(status_code=400, detail="Invalid model specified. Choose 'gemini' or 'openai'.")

        # Generate images based on model
        if request.model == "gemini":
            image_urls = await generate_image_gemini(request.prompt)
        else:  # openai
            image_urls = await generate_image_openai(request.prompt)

        saved_images = []
        for url in image_urls:
            file_path = await save_generated_image(url, request.prompt)
            saved_images.append({"url": url, "local_path": file_path})

        return {"message": "Images generated and saved successfully", "images": saved_images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
