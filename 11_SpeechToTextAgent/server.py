from __future__ import annotations

import os
import tempfile
import logging
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, Form, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import PORT, MAX_FILE_SIZE, SUPPORTED_AUDIO_FORMATS, SUPPORTED_VIDEO_FORMATS
from stt_service import transcribe_audio_file, get_supported_languages, SpeechToTextError
from audio_processor import process_media_file, cleanup_temp_files, get_file_info, AudioProcessingError
from youtube_processor import download_youtube_audio, validate_youtube_url, YouTubeProcessingError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SpeechToTextAgent")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
static_dir = os.path.join(BASE_DIR, "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Serve the main web interface."""
    try:
        languages = get_supported_languages()
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "languages": languages,
            },
        )
    except Exception as e:
        logger.error(f"Error serving index: {e}")
        # Return a basic error page if template loading fails
        return HTMLResponse(content=f"""
        <html>
            <body>
                <h1>SpeechToTextAgent Error</h1>
                <p>Failed to load the web interface: {str(e)}</p>
                <p>Please check your configuration and try again.</p>
            </body>
        </html>
        """, status_code=500)


@app.post("/api/transcribe")
async def transcribe_endpoint(
    file: Optional[UploadFile] = File(default=None),
    youtube_url: Optional[str] = Form(default=None),
    language: str = Form(default="auto"),
    include_timestamps: bool = Form(default=False),
):
    """
    Main transcription endpoint that handles file uploads and YouTube URLs.
    """
    temp_files = []  # Track temporary files for cleanup
    
    try:
        # Validate input
        if not file and not youtube_url:
            raise HTTPException(status_code=400, detail="Please provide either a file or YouTube URL")
        
        if file and youtube_url:
            raise HTTPException(status_code=400, detail="Please provide only one input method (file OR YouTube URL)")
        
        # Process YouTube URL
        if youtube_url:
            logger.info(f"Processing YouTube URL: {youtube_url}")
            
            # Validate YouTube URL
            is_valid, error_message = validate_youtube_url(youtube_url)
            if not is_valid:
                raise HTTPException(status_code=400, detail=error_message)
            
            # Download audio from YouTube
            audio_path, video_info = download_youtube_audio(youtube_url)
            temp_files.append(audio_path)
            
            # Get file info for response
            file_info = {
                "filename": f"YouTube: {video_info.get('title', 'Unknown')}",
                "size_mb": round(os.path.getsize(audio_path) / 1024 / 1024, 2),
                "is_video": True,
                "youtube_info": video_info
            }
            
            logger.info(f"YouTube audio downloaded: {file_info['filename']}")
        
        # Process uploaded file
        elif file:
            logger.info(f"Processing uploaded file: {file.filename}")
            
            # Validate file
            if not file.filename:
                raise HTTPException(status_code=400, detail="No filename provided")
            
            # Check file size
            file_size = 0
            file_content = b""
            
            # Read file content in chunks to get size
            while chunk := await file.read(8192):
                file_content += chunk
                file_size += len(chunk)
                if file_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"File size ({file_size / 1024 / 1024:.1f}MB) exceeds maximum allowed size (25MB)"
                    )
            
            # Save file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
                temp_files.append(temp_file_path)
            
            # Get file info
            file_info = get_file_info(temp_file_path)
            
            # Process the media file
            audio_path = process_media_file(temp_file_path, file_size)
            temp_files.append(audio_path)
            
            logger.info(f"File processed: {file_info['filename']}")
        
        # Perform transcription
        logger.info("Starting transcription...")
        transcription_result = transcribe_audio_file(
            audio_path, 
            language=language if language != "auto" else None,
            include_timestamps=include_timestamps
        )
        
        # Prepare response
        response_data = {
            "success": True,
            "transcription": transcription_result["text"],
            "language": transcription_result["language"],
            "duration": transcription_result["duration"],
            "model": transcription_result["model"],
            "file_info": file_info,
            "timestamp": include_timestamps
        }
        
        # Add YouTube info if applicable
        if youtube_url and "youtube_info" in file_info:
            response_data["youtube_info"] = file_info["youtube_info"]
        
        logger.info("Transcription completed successfully")
        return JSONResponse(content=response_data)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except SpeechToTextError as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except AudioProcessingError as e:
        logger.error(f"Audio processing error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except YouTubeProcessingError as e:
        logger.error(f"YouTube processing error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        # Clean up temporary files
        if temp_files:
            cleanup_temp_files(*temp_files)


@app.get("/api/languages")
async def get_languages():
    """Get list of supported languages."""
    try:
        languages = get_supported_languages()
        return JSONResponse(content={"languages": languages})
    except Exception as e:
        logger.error(f"Error getting languages: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve supported languages")


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check if OpenAI API key is configured
        from config import OPENAI_API_KEY
        if not OPENAI_API_KEY:
            return JSONResponse(
                content={"status": "error", "message": "OpenAI API key not configured"},
                status_code=503
            )
        
        return JSONResponse(content={"status": "healthy", "message": "SpeechToTextAgent is running"})
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            content={"status": "error", "message": f"Health check failed: {str(e)}"},
            status_code=503
        )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors."""
    return JSONResponse(
        content={"error": "Endpoint not found", "path": request.url.path},
        status_code=404
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        content={"error": "Internal server error", "message": "Something went wrong on our end"},
        status_code=500
    )


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting SpeechToTextAgent on port {PORT}")
    uvicorn.run("server:app", host="0.0.0.0", port=PORT, reload=False)
