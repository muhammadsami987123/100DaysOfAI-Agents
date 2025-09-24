import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration for PhotoOrganizerAgent."""
    PHOTO_EXTENSIONS = ['.jpg', '.jpeg', '.png']
    ORGANIZE_MODE = os.getenv('ORGANIZE_MODE', 'face')  # 'face' or 'location'
    MOCKED_FACES = ['Alice', 'Bob', 'Charlie', 'Diana']
    MOCKED_LOCATIONS = ['Paris', 'NewYork', 'Tokyo', 'Sydney']

CONFIG = Config()
