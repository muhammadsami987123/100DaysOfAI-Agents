import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MODEL_NAME = "gemini-2.0-flash-001"
    TEMPERATURE = 0.7
    MAX_TOKENS = 1500
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    LANGUAGE_OPTIONS = {
        "English": "en",
        "Urdu": "ur",
        "Hindi": "hi"
    }
    SUMMARY_FORMATS = {
        "Bullet Points": "bullet_points",
        "Key Takeaways": "key_takeaways",
        "Executive Summary": "executive_summary",
        "Action Items Only": "action_items_only"
    }
