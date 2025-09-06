"""
Web application for StoryWriterAgent using FastAPI
"""

from fastapi import FastAPI, HTTPException, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn
from pathlib import Path
import json

from config import StoryConfig

class StoryRequest(BaseModel):
    prompt: str
    genre: str = "fantasy"
    tone: str = "serious"
    length: str = "medium"
    language: str = "english"

class StoryResponse(BaseModel):
    success: bool
    story: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class StoryListResponse(BaseModel):
    success: bool
    stories: List[Dict[str, Any]] = []
    total: int = 0

def create_app(story_agent):
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=StoryConfig.WEB_TITLE,
        description=StoryConfig.WEB_DESCRIPTION,
        version=StoryConfig.WEB_VERSION
    )
    
    # Setup templates and static files
    templates = Jinja2Templates(directory="templates")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        """Serve the main story generation interface"""
        genres = story_agent.get_genres()
        tones = story_agent.get_tones()
        lengths = story_agent.get_lengths()
        languages = story_agent.get_languages()
        
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request,
                "genres": genres,
                "tones": tones,
                "lengths": lengths,
                "languages": languages
            }
        )
    
    @app.get("/stories", response_class=HTMLResponse)
    async def stories_page(request: Request):
        """Serve the stories management page"""
        stories = story_agent.get_story_list()
        favorites = story_agent.get_favorites()
        
        return templates.TemplateResponse(
            "stories.html",
            {
                "request": request,
                "stories": stories,
                "favorites": [f["id"] for f in favorites]
            }
        )
    
    @app.post("/api/generate", response_model=StoryResponse)
    async def generate_story(request: StoryRequest):
        """Generate a new story"""
        try:
            story = story_agent.generate_story(
                prompt=request.prompt,
                genre=request.genre,
                tone=request.tone,
                length=request.length,
                language=request.language
            )
            
            return StoryResponse(success=True, story=story)
            
        except Exception as e:
            return StoryResponse(success=False, error=str(e))
    
    @app.post("/api/save")
    async def save_story(
        story_id: str = Form(...),
        format: str = Form("both")
    ):
        """Save a story to file"""
        try:
            story = story_agent.get_story(story_id)
            if not story:
                raise HTTPException(status_code=404, detail="Story not found")
            
            saved_path = story_agent.save_story(story, format)
            if saved_path:
                return JSONResponse({
                    "success": True,
                    "message": f"Story saved to: {saved_path}",
                    "path": saved_path
                })
            else:
                return JSONResponse({
                    "success": False,
                    "error": "Failed to save story"
                })
                
        except Exception as e:
            return JSONResponse({
                "success": False,
                "error": str(e)
            })
    
    @app.get("/api/stories", response_model=StoryListResponse)
    async def get_stories():
        """Get list of all stories"""
        try:
            stories = story_agent.get_story_list()
            return StoryListResponse(
                success=True,
                stories=stories,
                total=len(stories)
            )
        except Exception as e:
            return StoryListResponse(
                success=False,
                stories=[],
                total=0
            )
    
    @app.get("/api/stories/{story_id}")
    async def get_story(story_id: str):
        """Get a specific story by ID"""
        try:
            story = story_agent.get_story(story_id)
            if story:
                return JSONResponse({
                    "success": True,
                    "story": story
                })
            else:
                return JSONResponse({
                    "success": False,
                    "error": "Story not found"
                })
        except Exception as e:
            return JSONResponse({
                "success": False,
                "error": str(e)
            })
    
    @app.post("/api/favorites/{story_id}")
    async def add_to_favorites(story_id: str):
        """Add a story to favorites"""
        try:
            success = story_agent.add_to_favorites(story_id)
            return JSONResponse({
                "success": success,
                "message": "Added to favorites" if success else "Already in favorites"
            })
        except Exception as e:
            return JSONResponse({
                "success": False,
                "error": str(e)
            })
    
    @app.delete("/api/favorites/{story_id}")
    async def remove_from_favorites(story_id: str):
        """Remove a story from favorites"""
        try:
            success = story_agent.remove_from_favorites(story_id)
            return JSONResponse({
                "success": success,
                "message": "Removed from favorites" if success else "Not in favorites"
            })
        except Exception as e:
            return JSONResponse({
                "success": False,
                "error": str(e)
            })
    
    @app.get("/api/favorites")
    async def get_favorites():
        """Get list of favorite stories"""
        try:
            favorites = story_agent.get_favorites()
            return JSONResponse({
                "success": True,
                "favorites": favorites
            })
        except Exception as e:
            return JSONResponse({
                "success": False,
                "error": str(e)
            })
    
    @app.delete("/api/stories/{story_id}")
    async def delete_story(story_id: str):
        """Delete a story"""
        try:
            success = story_agent.delete_story(story_id)
            return JSONResponse({
                "success": success,
                "message": "Story deleted" if success else "Story not found"
            })
        except Exception as e:
            return JSONResponse({
                "success": False,
                "error": str(e)
            })
    
    @app.get("/api/search")
    async def search_stories(q: str):
        """Search stories by query"""
        try:
            results = story_agent.search_stories(q)
            return JSONResponse({
                "success": True,
                "results": results,
                "total": len(results)
            })
        except Exception as e:
            return JSONResponse({
                "success": False,
                "error": str(e)
            })
    
    @app.get("/api/download/{story_id}")
    async def download_story(story_id: str, format: str = "txt"):
        """Download a story as a file"""
        try:
            story = story_agent.get_story(story_id)
            if not story:
                raise HTTPException(status_code=404, detail="Story not found")
            
            # Save story temporarily
            saved_path = story_agent.save_story(story, format)
            if not saved_path:
                raise HTTPException(status_code=500, detail="Failed to save story")
            
            # Return file
            file_path = Path(saved_path)
            return FileResponse(
                path=file_path,
                filename=file_path.name,
                media_type='text/plain' if format == 'txt' else 'text/markdown'
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/stats")
    async def get_stats():
        """Get statistics about stories"""
        try:
            stories = story_agent.get_story_list()
            favorites = story_agent.get_favorites()
            
            # Calculate stats
            total_stories = len(stories)
            total_favorites = len(favorites)
            
            # Genre distribution
            genre_counts = {}
            for story in stories:
                genre = story.get('genre', 'unknown')
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
            
            # Tone distribution
            tone_counts = {}
            for story in stories:
                tone = story.get('tone', 'unknown')
                tone_counts[tone] = tone_counts.get(tone, 0) + 1
            
            # Language distribution
            language_counts = {}
            for story in stories:
                language = story.get('language', 'unknown')
                language_counts[language] = language_counts.get(language, 0) + 1
            
            # Total word count
            total_words = sum(story.get('word_count', 0) for story in stories)
            
            return JSONResponse({
                "success": True,
                "stats": {
                    "total_stories": total_stories,
                    "total_favorites": total_favorites,
                    "total_words": total_words,
                    "genre_distribution": genre_counts,
                    "tone_distribution": tone_counts,
                    "language_distribution": language_counts
                }
            })
            
        except Exception as e:
            return JSONResponse({
                "success": False,
                "error": str(e)
            })
    
    @app.get("/api/export")
    async def export_stories(format: str = "json"):
        """Export all stories"""
        try:
            stories = story_agent.get_story_list()
            
            if format == "json":
                return JSONResponse({
                    "success": True,
                    "stories": stories,
                    "total": len(stories)
                })
            else:
                # For other formats, you could implement CSV, etc.
                return JSONResponse({
                    "success": False,
                    "error": f"Export format '{format}' not supported"
                })
                
        except Exception as e:
            return JSONResponse({
                "success": False,
                "error": str(e)
            })
    
    return app
