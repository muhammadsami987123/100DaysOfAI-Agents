import os
from dotenv import load_dotenv


load_dotenv()


def get_env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    return value


OPENAI_API_KEY = get_env("OPENAI_API_KEY")
TTS_ENGINE = (get_env("TTS_ENGINE", "openai") or "openai").lower()
PORT = int(get_env("PORT", "8009"))

# Voice preferences for OpenAI tts-1
DEFAULT_VOICE_FEMALE = "alloy"  # OpenAI TTS voice
DEFAULT_VOICE_MALE = "echo"      # OpenAI TTS voice

# Max characters to synthesize to avoid extremely long API calls
MAX_CHARACTERS = 8000


