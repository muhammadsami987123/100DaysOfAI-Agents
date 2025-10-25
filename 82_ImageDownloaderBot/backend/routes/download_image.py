from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional
from ..utils.file_handler import download_image_from_url
import re

router = APIRouter()

class DownloadImageRequest(BaseModel):
    url: str

    @property
    def is_valid_image_url(self) -> bool:
        # Check if URL ends with common image extensions
        image_extensions = r'\.(jpg|jpeg|png|gif|bmp|webp|svg)$'
        return bool(re.search(image_extensions, self.url, re.IGNORECASE))

    @property
    def is_base64_image(self) -> bool:
        # Check if the URL is actually a base64 image
        return self.url.startswith('data:image/')

@router.post("/download")
async def download_image(request: DownloadImageRequest):
    try:
        if not request.url or len(request.url.strip()) == 0:
            raise HTTPException(status_code=400, detail="URL cannot be empty")

        if not request.is_valid_image_url and not request.is_base64_image:
            raise HTTPException(
                status_code=400,
                detail="Invalid image URL. URL must end with a valid image extension (jpg, jpeg, png, gif, bmp, webp, svg) or be a base64 image"
            )

        file_path = await download_image_from_url(request.url)
        if not file_path:
            raise HTTPException(status_code=500, detail="Failed to save the downloaded image")

        return JSONResponse(
            status_code=200,
            content={
                "message": "Image downloaded successfully",
                "local_path": file_path
            }
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download image: {str(e)}")
