import os
from dotenv import load_dotenv

load_dotenv()

def _strip(val: str | None) -> str | None:
    if val is None:
        return None
    # Remove surrounding whitespace and surrounding quotes if present
    v = val.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        v = v[1:-1]
    return v


class Config:
    GEMINI_API_KEY = _strip(os.getenv("GEMINI_API_KEY"))
    OPENAI_API_KEY = _strip(os.getenv("OPENAI_API_KEY"))
    DEFAULT_LLM = _strip(os.getenv("DEFAULT_LLM", "gemini"))
    GEMINI_MODEL = _strip(os.getenv("GEMINI_MODEL", "gemini-2.0-flash"))
    OPENAI_MODEL = _strip(os.getenv("OPENAI_MODEL", "gpt-4.1"))
    DATA_DIR = _strip(os.getenv("DATA_DIR")) or "./data"
    DATA_FILE = os.path.join(DATA_DIR, "user_data.json")

