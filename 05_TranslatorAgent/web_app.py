from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from translator_agent import TranslatorAgent
from voice_service import VoiceService
from config import TranslatorConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="TranslatorAgent",
    description="AI-powered translation service with voice capabilities",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize services
translator = None
voice_service = None

# Pydantic models
class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "auto"
    target_lang: str = "en"
    style: str = "general"
    voice_enabled: bool = False

class LanguageDetectionRequest(BaseModel):
    text: str

class VoiceRequest(BaseModel):
    text: str
    language: str = "en"

class VoiceListenRequest(BaseModel):
    language: str = "en"
    timeout: int = 5

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global translator, voice_service
    
    try:
        # Initialize translator
        translator = TranslatorAgent()
        logger.info("TranslatorAgent initialized successfully")
        
        # Initialize voice service
        voice_service = VoiceService()
        logger.info("VoiceService initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main web interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/translate")
async def translate_text(request: TranslationRequest):
    """Translate text"""
    try:
        if not translator:
            raise HTTPException(status_code=500, detail="Translator not initialized")
        
        result = translator.translate_text(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            style=request.style
        )
        
        if result["success"]:
            # Get pronunciation if voice is enabled
            pronunciation = ""
            if request.voice_enabled:
                pronunciation = translator.get_pronunciation(
                    result["translation"], 
                    request.target_lang
                )
            
            return {
                "success": True,
                "translation": result["translation"],
                "original_text": result["original_text"],
                "source_lang": result["source_lang"],
                "target_lang": result["target_lang"],
                "source_name": result["source_name"],
                "target_name": result["target_name"],
                "pronunciation": pronunciation,
                "confidence": result["confidence"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/detect")
async def detect_language(request: LanguageDetectionRequest):
    """Detect language of text"""
    try:
        if not translator:
            raise HTTPException(status_code=500, detail="Translator not initialized")
        
        result = translator.detect_language(request.text)
        
        if result["success"]:
            return {
                "success": True,
                "detected_language": result["detected_language"],
                "language_name": result["language_name"],
                "confidence": result["confidence"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Language detection error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/languages")
async def get_languages():
    """Get supported languages"""
    try:
        if not translator:
            raise HTTPException(status_code=500, detail="Translator not initialized")
        
        languages = translator.get_supported_languages()
        return {"success": True, "languages": languages}
        
    except Exception as e:
        logger.error(f"Error getting languages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
async def get_history():
    """Get translation history"""
    try:
        if not translator:
            raise HTTPException(status_code=500, detail="Translator not initialized")
        
        history = translator.get_translation_history()
        return {"success": True, "history": history}
        
    except Exception as e:
        logger.error(f"Error getting history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/voice/speak")
async def speak_text(request: VoiceRequest):
    """Convert text to speech"""
    try:
        if not voice_service:
            raise HTTPException(status_code=500, detail="Voice service not initialized")
        
        # Log the speech request
        logger.info(f"Speech request: '{request.text[:50]}...' in {request.language}")
        
        # Validate input
        if not request.text or request.text.strip() == "":
            raise HTTPException(status_code=400, detail="No text provided to speak")
        
        result = voice_service.speak_text(request.text, request.language)
        
        if result["success"]:
            logger.info("Speech started successfully")
            return {
                "success": True,
                "text": result["text"],
                "language": result["language"],
                "speaking": result["speaking"]
            }
        else:
            logger.error(f"Speech failed: {result['error']}")
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Voice error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/voice/listen")
async def listen_for_speech(request: VoiceListenRequest):
    """Listen for speech and convert to text"""
    try:
        if not voice_service:
            raise HTTPException(status_code=500, detail="Voice service not initialized")
        
        logger.info(f"Listen request: language={request.language}, timeout={request.timeout}")
        
        result = voice_service.listen_for_speech(request.language, request.timeout)
        
        if result["success"]:
            logger.info(f"Speech recognized: '{result['text']}'")
            return {
                "success": True,
                "text": result["text"],
                "language": result["language"],
                "confidence": result["confidence"]
            }
        else:
            logger.warning(f"Speech recognition failed: {result['error']}")
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Speech recognition error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/voice/stop")
async def stop_speaking():
    """Stop ongoing speech"""
    try:
        if not voice_service:
            raise HTTPException(status_code=500, detail="Voice service not initialized")
        
        result = voice_service.stop_speaking()
        
        if result["success"]:
            return {
                "success": True,
                "stopped": result["stopped"],
                "message": result.get("message", "")
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Error stopping speech: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/voice/status")
async def get_voice_status():
    """Get detailed voice service status"""
    try:
        if not voice_service:
            raise HTTPException(status_code=500, detail="Voice service not initialized")
        
        result = voice_service.health_check()
        
        # Add troubleshooting tips
        troubleshooting = voice_service.get_troubleshooting_tips()
        result["troubleshooting"] = troubleshooting
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting voice status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/voice/test")
async def test_voice():
    """Test voice functionality"""
    try:
        if not voice_service:
            raise HTTPException(status_code=500, detail="Voice service not initialized")
        
        # Test with a simple text
        test_text = "Hello, this is a voice test."
        logger.info(f"Testing voice with text: '{test_text}'")
        
        result = voice_service.speak_text(test_text, "en")
        
        logger.info(f"Voice test result: {result}")
        
        return {
            "success": result["success"],
            "test_text": test_text,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Voice test error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        translator_health = translator.health_check() if translator else {"status": "unhealthy"}
        voice_health = voice_service.health_check() if voice_service else {"status": "unhealthy"}
        
        return {
            "status": "healthy" if (translator_health["status"] == "healthy" or voice_health["status"] == "healthy") else "unhealthy",
            "translator": translator_health,
            "voice": voice_health,
            "timestamp": "2024-01-15T12:00:00Z"  # You can use actual timestamp
        }
        
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "translator": {"status": "unhealthy"},
            "voice": {"status": "unhealthy"}
        }

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={"success": False, "error": "Endpoint not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    """Handle 500 errors"""
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "web_app:app",
        host=TranslatorConfig.HOST,
        port=TranslatorConfig.PORT,
        reload=TranslatorConfig.DEBUG
    ) 