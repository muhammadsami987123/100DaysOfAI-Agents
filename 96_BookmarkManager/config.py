import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration for BookmarkManager Agent"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # LLM Configuration
    DEFAULT_LLM = os.getenv("DEFAULT_LLM", "gemini")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Storage Configuration
    STORAGE_DIR = os.getenv("STORAGE_DIR", "./storage")
    BOOKMARKS_FILE = os.path.join(STORAGE_DIR, "bookmarks.json")
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # Ensure storage directory exists
    os.makedirs(STORAGE_DIR, exist_ok=True)

