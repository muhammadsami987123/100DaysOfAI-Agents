from agent import ScreenshotTakerAgent
from config import config

def main():
    """
    Main function to run the ScreenshotTakerAgent.
    """
    config.ensure_screenshots_dir_exists()
    agent = ScreenshotTakerAgent()
    agent.run()

if __name__ == "__main__":
    main()
