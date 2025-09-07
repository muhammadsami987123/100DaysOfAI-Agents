import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    serpapi_key: str = os.getenv("SERPAPI_API_KEY", "")
    google_cse_id: str = os.getenv("GOOGLE_CSE_ID", "")
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    data_dir: str = os.getenv("DATA_DIR", "data")

settings = Settings()
