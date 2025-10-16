import os
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = os.environ.get('LLM_MODEL', 'gemini')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


