import os

class Config:
    DEBUG = True
    PORT = 5000
    ALARM_FILE = 'alarms.json'
    # Add other configuration settings here, e.g., API keys for STT/TTS services
    # Example: GOOGLE_CLOUD_SPEECH_API_KEY = os.getenv('GOOGLE_CLOUD_SPEECH_API_KEY')
    # Example: OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
