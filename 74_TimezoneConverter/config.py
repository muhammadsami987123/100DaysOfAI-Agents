import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PROVIDER = os.environ.get("MODEL_PROVIDER", "gemini")
MODEL_NAME = os.environ.get("MODEL_NAME", "gemini-2.0-flash")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DEFAULT_SOURCE_TIMEZONE = os.environ.get("DEFAULT_SOURCE_TIMEZONE", "UTC")
DEFAULT_TARGET_TIMEZONE = os.environ.get("DEFAULT_TARGET_TIMEZONE", "Asia/Kolkata")
