import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Voice instructions and prompts
GREETING_MESSAGE = "Hello! I am App Uninstaller. You can say 'uninstall Zoom' to remove an app, or 'list apps' to see what's installed."
UNINSTALL_CONFIRMATION_PROMPT = "Are you sure you want to uninstall {}? Please say 'yes' or 'no'."
APP_NOT_FOUND_MESSAGE = "I could not find an app named {}. Please try again."
LIST_APPS_MESSAGE = "Here are the installed applications: "
UNINSTALL_SUCCESS_MESSAGE = "Successfully uninstalled {}."
UNINSTALL_FAILED_MESSAGE = "Failed to uninstall {}. Please check if the app is running or if you have administrative privileges."
NO_APPS_FOUND_MESSAGE = "No applications found matching your criteria."

# Other configurations
VOICE_INPUT_TIMEOUT = 5 # seconds
VOICE_INPUT_PHRASE_TIME_LIMIT = 10 # seconds
