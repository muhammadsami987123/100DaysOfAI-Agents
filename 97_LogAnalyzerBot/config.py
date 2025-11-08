"""
Configuration file for LogAnalyzerBot
Contains API keys, model settings, and application configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

# Application Settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.log', '.txt', '.json'}
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

# Log Parsing Configuration
LOG_LEVELS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE']
DEFAULT_DATE_FORMATS = [
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d %H:%M:%S.%f',
    '%Y/%m/%d %H:%M:%S',
    '%d/%b/%Y:%H:%M:%S',
    '%b %d %H:%M:%S',
    '%Y-%m-%dT%H:%M:%S',
    '%Y-%m-%dT%H:%M:%S.%fZ'
]

# Analysis Settings
MIN_PATTERN_FREQUENCY = 2  # Minimum occurrences to identify as pattern
MAX_SUGGESTIONS = 5  # Maximum number of suggestions to provide
