"""
Configuration and setup for StoryWriterAgent
"""

import os
from typing import Optional, Dict, Any

def get_api_key() -> Optional[str]:
    """Get OpenAI API key from environment variable or .env file"""
    # Try environment variable first
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key
    
    # Try .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return api_key
    except ImportError:
        pass
    
    return None

def setup_instructions():
    """Display setup instructions for API key"""
    print("🔧 Setup Instructions:")
    print("1. Get your OpenAI API key from: https://platform.openai.com/api-keys")
    print("2. Set the API key using one of these methods:")
    print("   Option A: Set environment variable:")
    print("     Windows: set OPENAI_API_KEY=your_api_key_here")
    print("     Linux/Mac: export OPENAI_API_KEY=your_api_key_here")
    print("   Option B: Create a .env file in the project root:")
    print("     OPENAI_API_KEY=your_api_key_here")
    print("   Option C: Create a config.json file:")
    print("     {\"openai_api_key\": \"your_api_key_here\"}")
    print()
    print("📚 After setting up the API key, run:")
    print("   python main.py --web        # Start web interface")
    print("   python main.py --terminal   # Start terminal interface")
    print("   python main.py --quick \"your prompt\"  # Quick story generation")

class StoryConfig:
    """Configuration constants for StoryWriterAgent"""
    
    # Available genres
    GENRES = {
        "fantasy": {
            "name": "Fantasy",
            "description": "Magical worlds, mythical creatures, and epic adventures",
            "keywords": ["magic", "dragons", "wizards", "enchanted", "kingdom", "quest"]
        },
        "sci-fi": {
            "name": "Science Fiction",
            "description": "Futuristic technology, space exploration, and scientific concepts",
            "keywords": ["space", "robot", "alien", "future", "technology", "galaxy"]
        },
        "mystery": {
            "name": "Mystery",
            "description": "Puzzles, investigations, and suspenseful plots",
            "keywords": ["detective", "clue", "secret", "investigation", "suspense", "crime"]
        },
        "romance": {
            "name": "Romance",
            "description": "Love stories and emotional relationships",
            "keywords": ["love", "heart", "relationship", "passion", "emotion", "couple"]
        },
        "horror": {
            "name": "Horror",
            "description": "Scary, suspenseful, and supernatural elements",
            "keywords": ["scary", "ghost", "monster", "dark", "fear", "nightmare"]
        },
        "children": {
            "name": "Children's Story",
            "description": "Kid-friendly stories with simple language and positive themes",
            "keywords": ["child", "adventure", "friendship", "learning", "fun", "happy"]
        }
    }
    
    # Available tones
    TONES = {
        "serious": {
            "name": "Serious",
            "description": "Thoughtful, profound, and meaningful storytelling",
            "style": "formal and contemplative"
        },
        "funny": {
            "name": "Funny",
            "description": "Humorous, light-hearted, and entertaining",
            "style": "witty and comedic"
        },
        "inspirational": {
            "name": "Inspirational",
            "description": "Uplifting, motivational, and encouraging",
            "style": "positive and empowering"
        },
        "dramatic": {
            "name": "Dramatic",
            "description": "Intense, emotional, and impactful",
            "style": "passionate and intense"
        }
    }
    
    # Story length options
    LENGTHS = {
        "short": {
            "name": "Short",
            "description": "1-2 paragraphs (100-300 words)",
            "paragraphs": 2,
            "words": 200
        },
        "medium": {
            "name": "Medium",
            "description": "3-5 paragraphs (300-600 words)",
            "paragraphs": 4,
            "words": 450
        },
        "long": {
            "name": "Long",
            "description": "7+ paragraphs (600+ words)",
            "paragraphs": 8,
            "words": 800
        }
    }
    
    # Supported languages
    LANGUAGES = {
        "english": {
            "name": "English",
            "code": "en",
            "description": "Generate stories in English"
        },
        "urdu": {
            "name": "Urdu",
            "code": "ur",
            "description": "Generate stories in Urdu (اردو)"
        },
        "arabic": {
            "name": "Arabic",
            "code": "ar",
            "description": "Generate stories in Arabic (العربية)"
        },
        "spanish": {
            "name": "Spanish",
            "code": "es",
            "description": "Generate stories in Spanish (Español)"
        },
        "french": {
            "name": "French",
            "code": "fr",
            "description": "Generate stories in French (Français)"
        },
        "german": {
            "name": "German",
            "code": "de",
            "description": "Generate stories in German (Deutsch)"
        }
    }
    
    # Default story settings
    DEFAULT_GENRE = "fantasy"
    DEFAULT_TONE = "serious"
    DEFAULT_LENGTH = "medium"
    DEFAULT_LANGUAGE = "english"
    
    # GPT settings
    MAX_TOKENS = 2000
    TEMPERATURE = 0.8
    
    # File storage settings
    STORIES_DIR = "stories"
    FAVORITES_FILE = "favorites.json"
    STORY_EXTENSIONS = [".txt", ".md"]
    
    # Web interface settings
    WEB_TITLE = "StoryWriterAgent"
    WEB_DESCRIPTION = "AI-powered creative story generation tool"
    WEB_VERSION = "1.0.0"
    
    # Story generation prompts
    STORY_PROMPTS = {
        "base": """You are a creative and skilled storyteller. Generate an engaging short story based on the following requirements:

Prompt: {prompt}
Genre: {genre}
Tone: {tone}
Length: {length} ({word_count} words approximately)
Language: {language}

Please create a story that:
1. Captures the essence of the prompt
2. Fits the specified genre with appropriate elements
3. Maintains the requested tone throughout
4. Is approximately {word_count} words long
5. Is written in {language}
6. Has a clear beginning, middle, and end
7. Is engaging and well-structured
8. Uses appropriate language for the target audience

Format the story with:
- A compelling title
- Proper paragraph breaks
- Clear narrative flow
- Appropriate dialogue if needed

Generate the story now:""",
        
        "multilingual": """You are a creative storyteller who can write in multiple languages. Generate a story in {language} based on:

Prompt: {prompt}
Genre: {genre}
Tone: {tone}
Length: {length} ({word_count} words approximately)

Requirements:
- Write entirely in {language}
- Use culturally appropriate references and expressions
- Maintain the genre and tone specifications
- Keep the story engaging and well-structured
- Include a title in {language}

Generate the story:"""
    }
