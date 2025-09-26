import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'a_very_secret_key_that_should_be_changed')
    # Example for shrtco.de (no API key needed for basic usage)
    # For other services like Bitly, you would add:
    # BITLY_API_KEY = os.getenv('BITLY_API_KEY')
    TINYURL_API_KEY = os.getenv('TINYURL_API_KEY')
    DEFAULT_SHORTENER_API = 'tinyurl' # Change to 'tinyurl' to use TinyURL
    QR_CODE_DIR = 'static/qrcodes'
    LANGUAGES = ['en', 'hi', 'ur']
    DEFAULT_LANGUAGE = 'en'
