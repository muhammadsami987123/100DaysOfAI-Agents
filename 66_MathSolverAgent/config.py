import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    ALLOWED_EXTENSIONS = {'txt', 'docx', 'pdf'}

    @classmethod
    def validate(cls):
        if not cls.GEMINI_API_KEY:
            print("⚠️ Warning: GEMINI_API_KEY not set in .env. Some features may not work.")
        return True
