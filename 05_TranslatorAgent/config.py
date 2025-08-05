import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TranslatorConfig:
    """Configuration settings for TranslatorAgent"""
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
    
    # Web Server Configuration
    HOST = os.getenv("TRANSLATOR_HOST", "127.0.0.1")
    PORT = int(os.getenv("TRANSLATOR_PORT", "8005"))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Voice Configuration
    VOICE_ENABLED = os.getenv("VOICE_ENABLED", "true").lower() == "true"
    SPEECH_RATE = int(os.getenv("SPEECH_RATE", "150"))
    VOICE_VOLUME = float(os.getenv("VOICE_VOLUME", "0.8"))
    
    # Translation Settings
    DEFAULT_SOURCE_LANG = "auto"
    DEFAULT_TARGET_LANG = "en"
    
    # Supported Languages
    SUPPORTED_LANGUAGES = {
        "en": {"name": "English", "native": "English"},
        "es": {"name": "Spanish", "native": "Español"},
        "fr": {"name": "French", "native": "Français"},
        "de": {"name": "German", "native": "Deutsch"},
        "it": {"name": "Italian", "native": "Italiano"},
        "pt": {"name": "Portuguese", "native": "Português"},
        "ru": {"name": "Russian", "native": "Русский"},
        "ja": {"name": "Japanese", "native": "日本語"},
        "ko": {"name": "Korean", "native": "한국어"},
        "zh": {"name": "Chinese", "native": "中文"},
        "ar": {"name": "Arabic", "native": "العربية"},
        "hi": {"name": "Hindi", "native": "हिन्दी"},
        "th": {"name": "Thai", "native": "ไทย"},
        "vi": {"name": "Vietnamese", "native": "Tiếng Việt"},
        "tr": {"name": "Turkish", "native": "Türkçe"},
        "pl": {"name": "Polish", "native": "Polski"},
        "nl": {"name": "Dutch", "native": "Nederlands"},
        "sv": {"name": "Swedish", "native": "Svenska"},
        "da": {"name": "Danish", "native": "Dansk"},
        "no": {"name": "Norwegian", "native": "Norsk"},
        "fi": {"name": "Finnish", "native": "Suomi"},
        "cs": {"name": "Czech", "native": "Čeština"},
        "hu": {"name": "Hungarian", "native": "Magyar"},
        "ro": {"name": "Romanian", "native": "Română"},
        "bg": {"name": "Bulgarian", "native": "Български"},
        "hr": {"name": "Croatian", "native": "Hrvatski"},
        "sk": {"name": "Slovak", "native": "Slovenčina"},
        "sl": {"name": "Slovenian", "native": "Slovenščina"},
        "et": {"name": "Estonian", "native": "Eesti"},
        "lv": {"name": "Latvian", "native": "Latviešu"},
        "lt": {"name": "Lithuanian", "native": "Lietuvių"},
        "mt": {"name": "Maltese", "native": "Malti"},
        "el": {"name": "Greek", "native": "Ελληνικά"},
        "he": {"name": "Hebrew", "native": "עברית"},
        "fa": {"name": "Persian", "native": "فارسی"},
        "ur": {"name": "Urdu", "native": "اردو"},
        "bn": {"name": "Bengali", "native": "বাংলা"},
        "ta": {"name": "Tamil", "native": "தமிழ்"},
        "te": {"name": "Telugu", "native": "తెలుగు"},
        "ml": {"name": "Malayalam", "native": "മലയാളം"},
        "kn": {"name": "Kannada", "native": "ಕನ್ನಡ"},
        "gu": {"name": "Gujarati", "native": "ગુજરાતી"},
        "pa": {"name": "Punjabi", "native": "ਪੰਜਾਬੀ"},
        "mr": {"name": "Marathi", "native": "मराठी"},
        "ne": {"name": "Nepali", "native": "नेपाली"},
        "si": {"name": "Sinhala", "native": "සිංහල"},
        "my": {"name": "Burmese", "native": "မြန်မာ"},
        "km": {"name": "Khmer", "native": "ខ្មែរ"},
        "lo": {"name": "Lao", "native": "ລາວ"},
        "mn": {"name": "Mongolian", "native": "Монгол"},
        "ka": {"name": "Georgian", "native": "ქართული"},
        "am": {"name": "Amharic", "native": "አማርኛ"},
        "sw": {"name": "Swahili", "native": "Kiswahili"},
        "zu": {"name": "Zulu", "native": "isiZulu"},
        "af": {"name": "Afrikaans", "native": "Afrikaans"},
        "sq": {"name": "Albanian", "native": "Shqip"},
        "hy": {"name": "Armenian", "native": "Հայերեն"},
        "az": {"name": "Azerbaijani", "native": "Azərbaycan"},
        "eu": {"name": "Basque", "native": "Euskara"},
        "be": {"name": "Belarusian", "native": "Беларуская"},
        "bs": {"name": "Bosnian", "native": "Bosanski"},
        "ca": {"name": "Catalan", "native": "Català"},
        "cy": {"name": "Welsh", "native": "Cymraeg"},
        "eo": {"name": "Esperanto", "native": "Esperanto"},
        "fo": {"name": "Faroese", "native": "Føroyskt"},
        "fy": {"name": "Frisian", "native": "Frysk"},
        "gl": {"name": "Galician", "native": "Galego"},
        "ga": {"name": "Irish", "native": "Gaeilge"},
        "is": {"name": "Icelandic", "native": "Íslenska"},
        "id": {"name": "Indonesian", "native": "Bahasa Indonesia"},
        "ia": {"name": "Interlingua", "native": "Interlingua"},
        "ie": {"name": "Interlingue", "native": "Interlingue"},
        "jv": {"name": "Javanese", "native": "Basa Jawa"},
        "kk": {"name": "Kazakh", "native": "Қазақ"},
        "ky": {"name": "Kyrgyz", "native": "Кыргызча"},
        "la": {"name": "Latin", "native": "Latina"},
        "lb": {"name": "Luxembourgish", "native": "Lëtzebuergesch"},
        "mk": {"name": "Macedonian", "native": "Македонски"},
        "ms": {"name": "Malay", "native": "Bahasa Melayu"},
        "mi": {"name": "Maori", "native": "Te Reo Māori"},
        "oc": {"name": "Occitan", "native": "Occitan"},
        "ps": {"name": "Pashto", "native": "پښتو"},
        "qu": {"name": "Quechua", "native": "Runa Simi"},
        "sm": {"name": "Samoan", "native": "Gagana Samoa"},
        "gd": {"name": "Scottish Gaelic", "native": "Gàidhlig"},
        "sr": {"name": "Serbian", "native": "Српски"},
        "st": {"name": "Sesotho", "native": "Sesotho"},
        "sn": {"name": "Shona", "native": "chiShona"},
        "sd": {"name": "Sindhi", "native": "سنڌي"},
        "so": {"name": "Somali", "native": "Soomaali"},
        "su": {"name": "Sundanese", "native": "Basa Sunda"},
        "tg": {"name": "Tajik", "native": "Тоҷикӣ"},
        "tt": {"name": "Tatar", "native": "Татар"},
        "tk": {"name": "Turkmen", "native": "Türkmençe"},
        "tw": {"name": "Twi", "native": "Twi"},
        "ug": {"name": "Uyghur", "native": "ئۇيغۇرچە"},
        "uz": {"name": "Uzbek", "native": "O'zbek"},
        "ve": {"name": "Venda", "native": "Tshivenda"},
        "xh": {"name": "Xhosa", "native": "isiXhosa"},
        "yi": {"name": "Yiddish", "native": "יידיש"},
        "yo": {"name": "Yoruba", "native": "Yorùbá"},
        "zu": {"name": "Zulu", "native": "isiZulu"}
    }
    
    @classmethod
    def get_language_name(cls, code: str) -> str:
        """Get language name by code"""
        return cls.SUPPORTED_LANGUAGES.get(code, {}).get("name", code)
    
    @classmethod
    def get_native_name(cls, code: str) -> str:
        """Get native language name by code"""
        return cls.SUPPORTED_LANGUAGES.get(code, {}).get("native", code)
    
    @classmethod
    def get_language_list(cls) -> List[Dict[str, str]]:
        """Get list of supported languages"""
        return [
            {"code": code, "name": info["name"], "native": info["native"]}
            for code, info in cls.SUPPORTED_LANGUAGES.items()
        ]
    
    @classmethod
    def is_supported(cls, code: str) -> bool:
        """Check if language code is supported"""
        return code in cls.SUPPORTED_LANGUAGES

# Translation prompts for different scenarios
TRANSLATION_PROMPTS = {
    "general": "Translate the following text from {source_lang} to {target_lang}. Maintain the original meaning, tone, and context. Provide a natural, fluent translation:",
    "formal": "Translate the following formal text from {source_lang} to {target_lang}. Use formal language and maintain professional tone:",
    "casual": "Translate the following casual text from {source_lang} to {target_lang}. Use natural, conversational language:",
    "technical": "Translate the following technical text from {source_lang} to {target_lang}. Maintain technical accuracy and terminology:",
    "literary": "Translate the following literary text from {source_lang} to {target_lang}. Preserve the artistic style and cultural nuances:"
}

# Voice settings for different languages
VOICE_SETTINGS = {
    "en": {"rate": 150, "voice": "en"},
    "es": {"rate": 140, "voice": "es"},
    "fr": {"rate": 145, "voice": "fr"},
    "de": {"rate": 140, "voice": "de"},
    "it": {"rate": 145, "voice": "it"},
    "pt": {"rate": 140, "voice": "pt"},
    "ja": {"rate": 130, "voice": "ja"},
    "ko": {"rate": 130, "voice": "ko"},
    "zh": {"rate": 130, "voice": "zh"},
    "ar": {"rate": 135, "voice": "ar"},
    "ru": {"rate": 140, "voice": "ru"}
} 