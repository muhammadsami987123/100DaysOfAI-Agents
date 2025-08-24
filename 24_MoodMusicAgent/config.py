"""
Configuration management for MoodMusicAgent
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for MoodMusicAgent"""
    
    # Project paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Create directories if they don't exist
    DATA_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Spotify API configuration
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback")
    
    # YouTube API configuration
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    
    # OpenAI API configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Local music settings
    LOCAL_MUSIC_PATH = os.getenv("LOCAL_MUSIC_PATH", str(BASE_DIR / "data" / "sample_music"))
    DEFAULT_VOLUME = float(os.getenv("DEFAULT_VOLUME", "0.7"))
    
    # Voice interface settings
    ENABLE_VOICE_INPUT = os.getenv("ENABLE_VOICE_INPUT", "true").lower() == "true"
    ENABLE_VOICE_OUTPUT = os.getenv("ENABLE_VOICE_OUTPUT", "true").lower() == "true"
    LANGUAGE = os.getenv("LANGUAGE", "en-US")
    
    # Mood history settings
    SAVE_MOOD_HISTORY = os.getenv("SAVE_MOOD_HISTORY", "true").lower() == "true"
    MOOD_HISTORY_FILE = DATA_DIR / os.getenv("MOOD_HISTORY_FILE", "mood_history.json")
    
    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / os.getenv("LOG_FILE", "mood_music_agent.log")
    
    # Mood categories and their music mappings
    MOOD_CATEGORIES = {
        "happy": {
            "description": "Upbeat, cheerful music",
            "genres": ["pop", "dance", "upbeat", "happy"],
            "energy_level": "high",
            "tempo": "fast",
            "volume_multiplier": 1.2
        },
        "sad": {
            "description": "Soothing, melancholic tunes",
            "genres": ["ambient", "slow", "melancholic", "indie"],
            "energy_level": "low",
            "tempo": "slow",
            "volume_multiplier": 0.8
        },
        "energetic": {
            "description": "High-energy, motivational tracks",
            "genres": ["rock", "electronic", "workout", "motivational"],
            "energy_level": "very_high",
            "tempo": "very_fast",
            "volume_multiplier": 1.4
        },
        "relaxed": {
            "description": "Calm, ambient sounds",
            "genres": ["ambient", "chill", "lofi", "nature"],
            "energy_level": "very_low",
            "tempo": "very_slow",
            "volume_multiplier": 0.6
        },
        "romantic": {
            "description": "Love songs and ballads",
            "genres": ["romantic", "ballad", "love", "soft"],
            "energy_level": "medium",
            "tempo": "medium",
            "volume_multiplier": 1.0
        },
        "stressed": {
            "description": "Calming, stress-relief music",
            "genres": ["meditation", "calm", "healing", "zen"],
            "energy_level": "very_low",
            "tempo": "very_slow",
            "volume_multiplier": 0.5
        },
        "motivated": {
            "description": "Inspirational, driving beats",
            "genres": ["inspirational", "motivational", "epic", "uplifting"],
            "energy_level": "high",
            "tempo": "fast",
            "volume_multiplier": 1.3
        },
        "focus": {
            "description": "Concentration-enhancing tracks",
            "genres": ["focus", "study", "instrumental", "classical"],
            "energy_level": "low",
            "tempo": "medium",
            "volume_multiplier": 0.9
        }
    }
    
    # Music source priorities
    MUSIC_SOURCES = ["spotify", "youtube", "local"]
    
    @classmethod
    def validate_config(cls):
        """Validate the configuration and return any issues"""
        issues = []
        
        # Check if at least one music source is configured
        if not cls.SPOTIFY_CLIENT_ID and not cls.YOUTUBE_API_KEY:
            issues.append("No music source configured. Please set up Spotify or YouTube API keys.")
        
        # Check local music path
        if not Path(cls.LOCAL_MUSIC_PATH).exists():
            issues.append(f"Local music path does not exist: {cls.LOCAL_MUSIC_PATH}")
        
        # Check voice interface dependencies
        if cls.ENABLE_VOICE_INPUT or cls.ENABLE_VOICE_OUTPUT:
            try:
                import speech_recognition
                import pyttsx3
            except ImportError:
                issues.append("Voice interface enabled but required packages not installed.")
        
        return issues
    
    @classmethod
    def get_mood_config(cls, mood):
        """Get configuration for a specific mood"""
        return cls.MOOD_CATEGORIES.get(mood.lower(), cls.MOOD_CATEGORIES["happy"])
    
    @classmethod
    def is_spotify_available(cls):
        """Check if Spotify is available"""
        return bool(cls.SPOTIFY_CLIENT_ID and cls.SPOTIFY_CLIENT_SECRET)
    
    @classmethod
    def is_youtube_available(cls):
        """Check if YouTube is available"""
        return bool(cls.YOUTUBE_API_KEY)
    
    @classmethod
    def is_openai_available(cls):
        """Check if OpenAI is available"""
        return bool(cls.OPENAI_API_KEY)
