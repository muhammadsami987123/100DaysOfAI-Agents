import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for MemoryNotesBot"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Application Configuration
    APP_NAME = "MemoryNotesBot"
    VERSION = "1.0.0"
    
    # Storage Configuration
    DATA_DIR = os.getenv("DATA_DIR", "./data")
    MEMORY_FILE = os.path.join(DATA_DIR, "memories.json")
    HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
    
    # Web UI Configuration
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Voice Configuration
    ENABLE_VOICE = os.getenv("ENABLE_VOICE", "True").lower() == "true"
    VOICE_TIMEOUT = int(os.getenv("VOICE_TIMEOUT", 5))
    
    # Memory Configuration
    MAX_MEMORIES = int(os.getenv("MAX_MEMORIES", 10000))
    SHORT_TERM_EXPIRY_HOURS = int(os.getenv("SHORT_TERM_EXPIRY_HOURS", 24))
    
    # Export Configuration
    EXPORT_DIR = os.path.join(DATA_DIR, "exports")
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.EXPORT_DIR, exist_ok=True)
