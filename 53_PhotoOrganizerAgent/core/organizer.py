import random
import os
import shutil
from config import CONFIG

class PhotoOrganizer:
    """Core logic for organizing photos by face or location (mocked)."""
    def __init__(self, mode:str = None):
        self.mode = mode or CONFIG.ORGANIZE_MODE

    def mock_detect(self, photo_path:str):
        if self.mode == 'face':
            return random.choice(CONFIG.MOCKED_FACES)
        else:
            return random.choice(CONFIG.MOCKED_LOCATIONS)

    def organize(self, source_dir:str):
        for filename in os.listdir(source_dir):
            if any(filename.lower().endswith(ext) for ext in CONFIG.PHOTO_EXTENSIONS):
                photo_path = os.path.join(source_dir, filename)
                detected = self.mock_detect(photo_path)
                target_folder = os.path.join(source_dir, detected)
                os.makedirs(target_folder, exist_ok=True)
                shutil.move(photo_path, os.path.join(target_folder, filename))
                print(f"Moved {filename} to {detected}/")
