import os

try:
    # Load variables from a local .env if present
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    # dotenv is optional; continue if not installed
    pass


class Config:
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Search (SerpAPI or NewsAPI)
    SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")

    # Timezone
    TIMEZONE = os.getenv("TW_TZ", "UTC")

    # Chrome Profile (for web automation)
    CHROME_PROFILE_PATH = os.getenv("CHROME_PROFILE_PATH", r"%LOCALAPPDATA%\Google\Chrome\User Data")
    CHROME_PROFILE_NAME = os.getenv("CHROME_PROFILE_NAME", "Default")

    # Social Media Platform Constraints
    PLATFORM_LIMITS = {
        "Twitter": 280,
        "Facebook": 63206,
        "Instagram": 2200,
        "LinkedIn": 3000,
        "TikTok": 150,
        "YouTube": 5000
    }
    
    # Default platform
    DEFAULT_PLATFORM = "Twitter"
    
    # Output directory for saved posts
    POSTS_DIR = "posts"


