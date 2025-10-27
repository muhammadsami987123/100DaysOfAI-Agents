import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEFAULT_LLM = os.getenv("DEFAULT_LLM", "gemini")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
