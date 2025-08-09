import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

DATA_DIR = BASE_DIR / 'data'
UPLOADS_DIR = DATA_DIR / 'uploads'
DOCS_DIR = DATA_DIR / 'docs'
STATIC_DIR = BASE_DIR / 'static'
TEMPLATES_DIR = BASE_DIR / 'templates'
LOGS_DIR = BASE_DIR / 'logs'

for d in (DATA_DIR, UPLOADS_DIR, DOCS_DIR, STATIC_DIR, TEMPLATES_DIR, LOGS_DIR):
    d.mkdir(parents=True, exist_ok=True)


@dataclass
class AppConfig:
    host: str = os.getenv('HOST', '127.0.0.1')
    port: int = int(os.getenv('PORT', '8000'))
    debug: bool = os.getenv('DEBUG', 'false').strip().lower() == 'true'

    openai_api_key: str | None = os.getenv('OPENAI_API_KEY')
    openai_model: str = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    embedding_model: str = os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')

    chunk_size_tokens: int = int(os.getenv('CHUNK_SIZE_TOKENS', '400'))
    chunk_overlap_tokens: int = int(os.getenv('CHUNK_OVERLAP_TOKENS', '40'))
    top_k: int = int(os.getenv('TOP_K', '6'))

    max_context_tokens: int = int(os.getenv('MAX_CONTEXT_TOKENS', '4000'))

    log_enabled: bool = os.getenv('LOG_ENABLED', 'true').strip().lower() == 'true'
    log_file: str = os.getenv('LOG_FILE', str(LOGS_DIR / 'pdfqa_log.jsonl'))


CONFIG = AppConfig()