import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration class for the ScreenshotTakerAgent.
    """
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SCREENSHOTS_DIR = "screenshots"

    @staticmethod
    def ensure_screenshots_dir_exists():
        """
        Ensures that the screenshots directory exists.
        """
        if not os.path.exists(Config.SCREENSHOTS_DIR):
            os.makedirs(Config.SCREENSHOTS_DIR)

config = Config()
config.ensure_screenshots_dir_exists()
