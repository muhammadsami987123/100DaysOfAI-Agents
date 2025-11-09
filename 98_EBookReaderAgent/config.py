"""
Configuration file for EBookReaderAgent
Contains API keys, model settings, and application configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()


def _strip(val: str | None) -> str | None:
    if val is None:
        return None
    # Remove surrounding whitespace and surrounding quotes if present
    v = val.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        v = v[1:-1]
    return v


class Config:
    """Application configuration"""
    
    # API Configuration
    GEMINI_API_KEY = _strip(os.getenv("GEMINI_API_KEY"))
    OPENAI_API_KEY = _strip(os.getenv("OPENAI_API_KEY"))
    DEFAULT_LLM = _strip(os.getenv("DEFAULT_LLM", "gemini"))
    GEMINI_MODEL = _strip(os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp"))
    OPENAI_MODEL = _strip(os.getenv("OPENAI_MODEL", "gpt-4o"))
    
    # Application Settings
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'.pdf', '.epub'}
    UPLOAD_FOLDER = "uploads"
    OUTPUT_FOLDER = "outputs"
    
    # Reading Settings
    WORDS_PER_MINUTE = 200  # Average reading speed
    MAX_CHAPTER_LENGTH = 10000  # Max characters per chapter for processing
    SUMMARY_LENGTH = 500  # Target summary length in words
