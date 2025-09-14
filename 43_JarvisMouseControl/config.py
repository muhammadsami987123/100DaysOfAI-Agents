"""
Configuration management for JarvisMouseControl
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

@dataclass
class MouseControlConfig:
    """Configuration class for JarvisMouseControl"""
    
    # Project paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    UTILS_DIR = BASE_DIR / "utils"
    
    # Create directories if they don't exist
    DATA_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    # OpenAI API configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "500"))
    
    # Voice recognition settings
    VOICE_ENABLED = os.getenv("VOICE_ENABLED", "true").lower() == "true"
    VOICE_TIMEOUT = float(os.getenv("VOICE_TIMEOUT", "2.0"))  # Reduced for better responsiveness
    VOICE_PHRASE_TIMEOUT = float(os.getenv("VOICE_PHRASE_TIMEOUT", "0.3"))
    VOICE_ENERGY_THRESHOLD = int(os.getenv("VOICE_ENERGY_THRESHOLD", "300"))
    
    # Text-to-speech settings
    TTS_ENABLED = os.getenv("TTS_ENABLED", "true").lower() == "true"
    TTS_RATE = int(os.getenv("TTS_RATE", "180"))
    TTS_VOLUME = float(os.getenv("TTS_VOLUME", "0.8"))
    TTS_VOICE_ID = os.getenv("TTS_VOICE_ID", "0")  # 0 for default voice
    
    # Language settings
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
    SUPPORTED_LANGUAGES = ["en", "ur", "hi"]
    LANGUAGE_NAMES = {
        "en": "English",
        "ur": "Urdu",
        "hi": "Hindi"
    }
    
    # Mouse control settings
    MOUSE_SPEED = float(os.getenv("MOUSE_SPEED", "1.0"))
    MOUSE_DURATION = float(os.getenv("MOUSE_DURATION", "0.5"))
    SCROLL_AMOUNT = int(os.getenv("SCROLL_AMOUNT", "3"))
    CLICK_DELAY = float(os.getenv("CLICK_DELAY", "0.1"))
    
    # Safety settings
    ENABLE_SAFETY = os.getenv("ENABLE_SAFETY", "true").lower() == "true"
    SAFETY_BOUNDS = {
        "min_x": 0,
        "min_y": 0,
        "max_x": 1920,  # Default screen width
        "max_y": 1080   # Default screen height
    }
    
    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / "jarvis_mouse.log"
    
    # Translation file path
    TRANSLATIONS_FILE = UTILS_DIR / "translations.json"
    
    # Command patterns for different languages
    COMMAND_PATTERNS = {
        "en": {
            "move_up": ["move up", "go up", "scroll up", "move cursor up"],
            "move_down": ["move down", "go down", "scroll down", "move cursor down"],
            "move_left": ["move left", "go left", "move cursor left"],
            "move_right": ["move right", "go right", "move cursor right"],
            "click": ["click", "left click", "click here", "press"],
            "double_click": ["double click", "double-click", "double press"],
            "right_click": ["right click", "right-click", "context menu"],
            "scroll_up": ["scroll up", "scroll up page", "page up"],
            "scroll_down": ["scroll down", "scroll down page", "page down"],
            "drag": ["drag", "drag and drop", "move while holding"],
            "stop": ["stop", "quit", "exit", "end", "cancel"]
        },
        "ur": {
            "move_up": ["اوپر جاؤ", "اوپر چلو", "اوپر سکرول کرو"],
            "move_down": ["نیچے جاؤ", "نیچے چلو", "نیچے سکرول کرو"],
            "move_left": ["بائیں جاؤ", "بائیں چلو"],
            "move_right": ["دائیں جاؤ", "دائیں چلو"],
            "click": ["کلک کرو", "دباؤ", "پریس کرو"],
            "double_click": ["دو بار کلک کرو", "ڈبل کلک کرو"],
            "right_click": ["دائیں کلک کرو", "رائٹ کلک کرو"],
            "scroll_up": ["اوپر سکرول کرو", "صفحہ اوپر کرو"],
            "scroll_down": ["نیچے سکرول کرو", "صفحہ نیچے کرو"],
            "drag": ["کھینچو", "ڈریگ کرو"],
            "stop": ["رکو", "بند کرو", "ختم کرو"]
        },
        "hi": {
            "move_up": ["ऊपर जाओ", "ऊपर चलो", "ऊपर स्क्रॉल करो"],
            "move_down": ["नीचे जाओ", "नीचे चलो", "नीचे स्क्रॉल करो"],
            "move_left": ["बाएं जाओ", "बाएं चलो"],
            "move_right": ["दाएं जाओ", "दाएं चलो"],
            "click": ["क्लिक करो", "दबाओ", "प्रेस करो"],
            "double_click": ["दो बार क्लिक करो", "डबल क्लिक करो"],
            "right_click": ["दाएं क्लिक करो", "राइट क्लिक करो"],
            "scroll_up": ["ऊपर स्क्रॉल करो", "पेज ऊपर करो"],
            "scroll_down": ["नीचे स्क्रॉल करो", "पेज नीचे करो"],
            "drag": ["खींचो", "ड्रैग करो"],
            "stop": ["रुको", "बंद करो", "समाप्त करो"]
        }
    }
    
    # Mouse action mappings
    MOUSE_ACTIONS = {
        "move_up": "move_up",
        "move_down": "move_down", 
        "move_left": "move_left",
        "move_right": "move_right",
        "click": "click",
        "double_click": "double_click",
        "right_click": "right_click",
        "scroll_up": "scroll_up",
        "scroll_down": "scroll_down",
        "drag": "drag",
        "stop": "stop"
    }
    
    # Movement distances (in pixels)
    MOVE_DISTANCES = {
        "small": 50,
        "medium": 100,
        "large": 200
    }
    
    # Feedback messages
    FEEDBACK_MESSAGES = {
        "en": {
            "listening": "🎤 Listening for voice commands...",
            "command_recognized": "✅ Command recognized: {command}",
            "action_executed": "🖱️ Action executed: {action}",
            "error_recognizing": "❌ Could not recognize command. Please try again.",
            "error_executing": "❌ Error executing action: {error}",
            "safety_stop": "🛑 Safety stop activated. Command not executed.",
            "language_changed": "🌍 Language changed to: {language}",
            "voice_disabled": "🔇 Voice input disabled. Use text commands.",
            "tts_disabled": "🔇 Voice feedback disabled."
        },
        "ur": {
            "listening": "🎤 آواز کے حکم سن رہا ہوں...",
            "command_recognized": "✅ حکم پہچان لیا: {command}",
            "action_executed": "🖱️ عمل انجام دیا: {action}",
            "error_recognizing": "❌ حکم پہچان نہیں سکا۔ دوبارہ کوشش کریں۔",
            "error_executing": "❌ عمل انجام دینے میں خرابی: {error}",
            "safety_stop": "🛑 حفاظتی رکاوٹ۔ حکم انجام نہیں دیا گیا۔",
            "language_changed": "🌍 زبان تبدیل ہو گئی: {language}",
            "voice_disabled": "🔇 آواز کا ان پٹ بند ہے۔ متن کے حکم استعمال کریں۔",
            "tts_disabled": "🔇 آواز کا جواب بند ہے۔"
        },
        "hi": {
            "listening": "🎤 आवाज़ के आदेश सुन रहा हूं...",
            "command_recognized": "✅ आदेश पहचाना: {command}",
            "action_executed": "🖱️ कार्य किया: {action}",
            "error_recognizing": "❌ आदेश पहचान नहीं सका। कृपया फिर से कोशिश करें।",
            "error_executing": "❌ कार्य करने में त्रुटि: {error}",
            "safety_stop": "🛑 सुरक्षा रोक सक्रिय। आदेश नहीं किया गया।",
            "language_changed": "🌍 भाषा बदली: {language}",
            "voice_disabled": "🔇 आवाज़ इनपुट बंद है। टेक्स्ट आदेश का उपयोग करें।",
            "tts_disabled": "🔇 आवाज़ फीडबैक बंद है।"
        }
    }

def get_api_key() -> Optional[str]:
    """Get OpenAI API key from environment variable or .env file"""
    # Try environment variable first
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key
    
    # Try .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return api_key
    except ImportError:
        pass
    
    return None

def setup_instructions():
    """Display setup instructions for API key"""
    print("🔧 Setup Instructions:")
    print("1. Get your OpenAI API key from: https://platform.openai.com/api-keys")
    print("2. Set the API key using one of these methods:")
    print("   Option A: Set environment variable:")
    print("     Windows: set OPENAI_API_KEY=your_api_key_here")
    print("     Linux/Mac: export OPENAI_API_KEY=your_api_key_here")
    print("   Option B: Create a .env file in the project root:")
    print("     OPENAI_API_KEY=your_api_key_here")
    print()
    print("🎤 After setting up the API key, run:")
    print("   python main.py --language en    # English mode")
    print("   python main.py --language ur    # Urdu mode")
    print("   python main.py --language hi    # Hindi mode")
    print("   python main.py --help           # Show all options")

# Global config instance
CONFIG = MouseControlConfig()
