import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")  # Using GOOGLE_API_KEY from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LLM Models
GEMINI_MODEL = "gemini-2.0-flash"  # Or "gemini-1.5-flash"
OPENAI_MODEL = "gpt-4"

# Paths
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")
CHAPTERS_DIR = os.path.join(os.path.dirname(__file__), "chapters")
TRANSCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "transcripts")

# Create directories if they don't exist
for directory in [UPLOAD_DIR, PROMPTS_DIR, CHAPTERS_DIR, TRANSCRIPTS_DIR]:
    os.makedirs(directory, exist_ok=True)
