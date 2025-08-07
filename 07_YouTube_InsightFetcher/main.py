import re
import sys
import os
import platform
import pyperclip
from typing import Optional
from colorama import init, Fore, Style
init(autoreset=True)

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
except ImportError:
    print("youtube_transcript_api not found. Please install it with 'pip install youtube-transcript-api'.")
    sys.exit(1)

try:
    import openai
except ImportError:
    print("openai package not found. Please install it with 'pip install openai'.")
    sys.exit(1)

try:
    from langdetect import detect
except ImportError:
    print("langdetect package not found. Please install it with 'pip install langdetect'.")
    sys.exit(1)

from cli import run_cli

if __name__ == "__main__":
    run_cli()
