"""
Configuration and setup for ArticleRewriter
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for ArticleRewriter"""
    
    # API Configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini")  # gemini or openai
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = 8075
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # UI Configuration
    APP_TITLE = "ArticleRewriter"
    APP_DESCRIPTION = "AI-powered article rewriting tool with multiple tone options"
    APP_VERSION = "1.0.0"
    
    # Available tones for rewriting
    TONES = {
        "formal": {
            "name": "Formal",
            "description": "Professional, academic, and business-appropriate tone",
            "keywords": ["professional", "academic", "business", "official", "serious"]
        },
        "casual": {
            "name": "Casual",
            "description": "Relaxed, conversational, and friendly tone",
            "keywords": ["friendly", "conversational", "relaxed", "informal", "chatty"]
        },
        "professional": {
            "name": "Professional",
            "description": "Business-focused, clear, and authoritative tone",
            "keywords": ["business", "corporate", "authoritative", "clear", "precise"]
        },
        "witty": {
            "name": "Witty",
            "description": "Clever, humorous, and engaging tone with personality",
            "keywords": ["humorous", "clever", "engaging", "personality", "fun"]
        },
        "poetic": {
            "name": "Poetic",
            "description": "Artistic, flowing, and emotionally expressive tone",
            "keywords": ["artistic", "flowing", "emotional", "expressive", "beautiful"]
        },
        "persuasive": {
            "name": "Persuasive",
            "description": "Convincing, compelling, and sales-oriented tone",
            "keywords": ["convincing", "compelling", "sales", "influential", "motivating"]
        },
        "simplified": {
            "name": "Simplified",
            "description": "Clear, simple, and easy-to-understand tone",
            "keywords": ["simple", "clear", "easy", "accessible", "straightforward"]
        }
    }
    
    # Available languages
    LANGUAGES = {
        "english": {
            "name": "English",
            "code": "en",
            "description": "Rewrite in English"
        },
        "urdu": {
            "name": "Urdu",
            "code": "ur",
            "description": "Rewrite in Urdu (اردو)"
        },
        "spanish": {
            "name": "Spanish",
            "code": "es",
            "description": "Rewrite in Spanish (Español)"
        },
        "french": {
            "name": "French",
            "code": "fr",
            "description": "Rewrite in French (Français)"
        },
        "german": {
            "name": "German",
            "code": "de",
            "description": "Rewrite in German (Deutsch)"
        },
        "arabic": {
            "name": "Arabic",
            "code": "ar",
            "description": "Rewrite in Arabic (العربية)"
        }
    }
    
    # Default settings
    DEFAULT_TONE = "formal"
    DEFAULT_LANGUAGE = "english"
    
    # GPT settings
    MAX_TOKENS = 2000
    TEMPERATURE = 0.7
    
    # File storage settings
    OUTPUTS_DIR = "outputs"
    OUTPUT_EXTENSIONS = [".txt", ".md"]
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if cls.LLM_MODEL.lower() == "gemini":
            if not cls.GEMINI_API_KEY:
                print("⚠️ Warning: GEMINI_API_KEY not found. AI features will be limited.")
                return False
        elif cls.LLM_MODEL.lower() == "openai":
            if not cls.OPENAI_API_KEY:
                print("⚠️ Warning: OPENAI_API_KEY not found. AI features will be limited.")
                return False
        else:
            print("⚠️ Warning: No valid LLM model configured. AI features will be limited.")
            return False
        return True
    
    @classmethod
    def get_tone_description(cls, tone: str) -> str:
        """Get description for a specific tone"""
        return cls.TONES.get(tone, {}).get("description", "Unknown tone")
    
    @classmethod
    def get_language_name(cls, lang_code: str) -> str:
        """Get language name from code"""
        for lang in cls.LANGUAGES.values():
            if lang["code"] == lang_code:
                return lang["name"]
        return "Unknown"
    
    @classmethod
    def get_available_tones(cls) -> Dict[str, Dict[str, str]]:
        """Get available tones for rewriting"""
        return cls.TONES
    
    @classmethod
    def get_available_languages(cls) -> Dict[str, Dict[str, str]]:
        """Get available languages for rewriting"""
        return cls.LANGUAGES
