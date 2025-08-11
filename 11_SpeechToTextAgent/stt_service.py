import os
import logging
from typing import Optional, Dict, Any
from openai import OpenAI
from config import OPENAI_API_KEY, WHISPER_MODEL, DEFAULT_LANGUAGE, INCLUDE_TIMESTAMPS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpeechToTextError(Exception):
    """Custom exception for speech-to-text errors."""
    pass


class WhisperService:
    """Service for handling OpenAI Whisper API transcription."""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise SpeechToTextError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
        
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = WHISPER_MODEL
        logger.info(f"Initialized Whisper service with model: {self.model}")
    
    def transcribe_audio(self, audio_file_path: str, language: Optional[str] = None, 
                        include_timestamps: bool = False) -> Dict[str, Any]:
        """
        Transcribe audio file using OpenAI Whisper API.
        
        Args:
            audio_file_path: Path to the audio file
            language: Language hint for transcription (optional)
            include_timestamps: Whether to include timestamps in output
            
        Returns:
            Dictionary containing transcription results
        """
        try:
            logger.info(f"Starting transcription of: {audio_file_path}")
            
            # Prepare transcription options
            transcription_options = {
                "model": self.model,
                "file": open(audio_file_path, "rb"),
                "response_format": "verbose_json" if include_timestamps else "json",
                "language": language if language and language != "auto" else None,
                "prompt": self._get_language_prompt(language)
            }
            
            # Remove None values
            transcription_options = {k: v for k, v in transcription_options.items() if v is not None}
            
            # Perform transcription
            logger.info("Sending audio to OpenAI Whisper API...")
            response = self.client.audio.transcriptions.create(**transcription_options)
            
            # Process response
            if include_timestamps and hasattr(response, 'segments'):
                # Format with timestamps
                formatted_text = self._format_with_timestamps(response.segments)
                segments = response.segments
            else:
                # Simple text output
                formatted_text = response.text
                segments = None
            
            # Prepare result
            result = {
                "text": formatted_text,
                "language": getattr(response, 'language', 'unknown'),
                "duration": getattr(response, 'duration', 0),
                "segments": segments,
                "model": self.model,
                "success": True
            }
            
            _lang = getattr(response, 'language', language or 'unknown')
            _dur = getattr(response, 'duration', 0)
            logger.info(f"Transcription completed successfully. Language: {_lang}, Duration: {_dur}s")
            return result
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise SpeechToTextError(f"Transcription failed: {str(e)}")
        finally:
            # Ensure file is closed
            if 'file' in locals():
                transcription_options['file'].close()
    
    def _format_with_timestamps(self, segments: list) -> str:
        """
        Format transcription segments with timestamps.
        
        Args:
            segments: List of transcription segments from Whisper API
            
        Returns:
            Formatted text with timestamps
        """
        if not segments:
            return ""
        
        formatted_lines = []
        for segment in segments:
            start_time = self._format_timestamp(segment.start)
            end_time = self._format_timestamp(segment.end)
            text = segment.text.strip()
            
            if text:
                formatted_lines.append(f"[{start_time} - {end_time}] {text}")
        
        return "\n".join(formatted_lines)
    
    def _format_timestamp(self, seconds: float) -> str:
        """
        Format seconds to MM:SS format.
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted timestamp string
        """
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes:02d}:{remaining_seconds:02d}"
    
    def _get_language_prompt(self, language: Optional[str]) -> str:
        """
        Get language-specific prompt for better transcription quality.
        
        Args:
            language: Language code
            
        Returns:
            Language-specific prompt string
        """
        if not language or language == "auto":
            return "This is a transcription. Please provide clean, well-formatted text with proper punctuation."
        
        language_prompts = {
            "hi": "यह एक ट्रांसक्रिप्शन है। कृपया साफ, अच्छी तरह से स्वरूपित पाठ प्रदान करें जिसमें उचित विराम चिह्न हों।",
            "ur": "یہ ایک ٹرانسکرپشن ہے۔ براہ کرم صاف، اچھی طرح سے فارمیٹڈ ٹیکسٹ فراہم کریں جس میں مناسب اوقاف ہوں۔",
            "bn": "এটি একটি ট্রান্সক্রিপশন। অনুগ্রহ করে পরিষ্কার, সুন্দরভাবে ফরম্যাট করা পাঠ্য সরবরাহ করুন যাতে সঠিক বিরাম চিহ্ন থাকে।",
            "ta": "இது ஒரு டிரான்ஸ்கிரிப்ஷன். தயவுசெய்து தெளிவான, நன்கு வடிவமைக்கப்பட்ட உரையை சரியான நிறுத்தக்குறிகளுடன் வழங்கவும்.",
            "te": "ఇది ఒక ట్రాన్స్క్రిప్షన్. దయచేసి స్పష్టమైన, బాగా ఫార్మాట్ చేయబడిన వచనాన్ని సరైన విరామ చిహ్నాలతో అందించండి.",
            "kn": "ಇದು ಒಂದು ಟ್ರಾನ್ಸ್ಕ್ರಿಪ್ಷನ್. ದಯವಿಟ್ಟು ಸ್ಪಷ್ಟವಾದ, ಚೆನ್ನಾಗಿ ಫಾರ್ಮ್ಯಾಟ್ ಮಾಡಲಾದ ಪಠ್ಯವನ್ನು ಸರಿಯಾದ ವಿರಾಮ ಚಿಹ್ನೆಗಳೊಂದಿಗೆ ಒದಗಿಸಿ.",
            "ml": "ഇത് ഒരു ട്രാൻസ്ക്രിപ്ഷൻ ആണ്. ദയവായി വ്യക്തമായ, നന്നായി ഫോർമാറ്റ് ചെയ്ത വാചകം ശരിയായ വിരാമ ചിഹ്നങ്ങളോടെ നൽകുക.",
            "gu": "આ એક ટ્રાન્સક્રિપ્શન છે. કૃપા કરીને સ્પષ્ટ, સારી રીતે ફોર્મેટ કરેલ ટેક્સ્ટ યોગ્ય વિરામ ચિહ્નો સાથે આપો.",
            "pa": "ਇਹ ਇੱਕ ਟ੍ਰਾਂਸਕ੍ਰਿਪਸ਼ਨ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਸਪਸ਼ਟ, ਚੰਗੀ ਤਰ੍ਹਾਂ ਫਾਰਮੈਟ ਕੀਤਾ ਟੈਕਸਟ ਯੋਗਿਕ ਵਿਰਾਮ ਚਿੰਨ੍ਹਾਂ ਨਾਲ ਦਿਓ।",
            "or": "ଏହା ଏକ ଟ୍ରାନ୍ସକ୍ରିପସନ୍। ଦୟାକରି ସ୍ପଷ୍ଟ, ଭଲ ଭାବରେ ଫର୍ମାଟ କରାଯାଇଥିବା ପାଠ ଯଥାର୍ଥ ବିରାਮ ଚିହ୍ନ ସହିତ ପ୍ରଦାନ କରନ୍ତୁ।",
            "as": "এই এটা ট্ৰান্সক্ৰিপচন। অনুগ্ৰহ কৰি পৰিষ্কাৰ, ভালদৰে ফৰ্মেট কৰা পাঠ্য সঠিক বিৰাম চিহ্নৰ সৈতে যোগান ধৰক।",
            "ne": "यो एउटा ट्रान्सक्रिप्सन हो। कृपया सफा, राम्रोसँग फर्मेट गरिएको पाठ उचित विराम चिह्नहरूसँग प्रदान गर्नुहोस्।",
            "si": "මෙය ට්‍රාන්ස්ක්‍රිප්ෂනයකි. කරුණාකර පැහැදිලි, හොඳින් ආකෘතිගත කර ඇති පාඨය නිවැරදි විරා ලකුණු සමඟ සපයන්න.",
            "my": "ဒါဟာ ထရန်စကရစ်ပရှင်တစ်ခုဖြစ်ပါတယ်။ ကျေးဇူးပြု၍ ရှင်းလင်းပြီး ကောင်းမွန်စွာ ဖော်မတ်ထားသော စာသားကို သင့်လျော်သော ရပ်တန့်ခြင်း သင်္ကေတများနှင့် ပေးပါ။",
            "km": "នេះគឺជាការចម្លង។ សូមផ្តល់អត្ថបទដែលមានភាពច្បាស់លាស់ ដែលបានរៀបចំឱ្យបានល្អ ជាមួយនឹងសញ្ញាការឈប់ដែលសមស្រប។",
            "lo": "ນີ້ແມ່ນການຂຽນຄຳເວົ້າ. ກະລຸນາໃຫ້ຂໍ້ຄວາມທີ່ຊັດເຈນ, ທີ່ຈັດຮູບແບບໄວ້ດີ ພ້ອມກັບເຄື່ອງໝາຍຈຸດທີ່ເໝາະສົມ.",
            "th": "นี่คือการถอดความ กรุณาให้ข้อความที่ชัดเจน จัดรูปแบบไว้ดี พร้อมเครื่องหมายวรรคตอนที่เหมาะสม",
            "vi": "Đây là một bản ghi chép. Vui lòng cung cấp văn bản rõ ràng, được định dạng tốt với dấu câu thích hợp.",
            "id": "Ini adalah transkripsi. Harap berikan teks yang jelas dan diformat dengan baik dengan tanda baca yang tepat.",
            "ms": "Ini adalah transkripsi. Sila berikan teks yang jelas dan diformat dengan baik dengan tanda baca yang sesuai.",
            "tl": "Ito ay isang transkripsyon. Mangyaring magbigay ng malinaw, maayos na na-format na teksto na may angkop na mga bantas.",
            "en": "This is a transcription. Please provide clean, well-formatted text with proper punctuation."
        }
        
        return language_prompts.get(language, "This is a transcription. Please provide clean, well-formatted text with proper punctuation.")
    
    def get_supported_languages(self) -> list:
        """
        Get list of supported languages for transcription.
        
        Returns:
            List of supported language codes
        """
        # Whisper supports 100+ languages, here are the most common ones
        return [
            {"code": "auto", "name": "Auto-detect", "native": "Auto-detect"},
            {"code": "en", "name": "English", "native": "English"},
            {"code": "es", "name": "Spanish", "native": "Español"},
            {"code": "fr", "name": "French", "native": "Français"},
            {"code": "de", "name": "German", "native": "Deutsch"},
            {"code": "it", "name": "Italian", "native": "Italiano"},
            {"code": "pt", "name": "Portuguese", "native": "Português"},
            {"code": "ru", "name": "Russian", "native": "Русский"},
            {"code": "ja", "name": "Japanese", "native": "日本語"},
            {"code": "ko", "name": "Korean", "native": "한국어"},
            {"code": "zh", "name": "Chinese", "native": "中文"},
            {"code": "ar", "name": "Arabic", "native": "العربية"},
            {"code": "hi", "name": "Hindi", "native": "हिन्दी"},
            {"code": "ur", "name": "Urdu", "native": "اردو"},
            {"code": "tr", "name": "Turkish", "native": "Türkçe"},
            {"code": "nl", "name": "Dutch", "native": "Nederlands"},
            {"code": "pl", "name": "Polish", "native": "Polski"},
            {"code": "sv", "name": "Swedish", "native": "Svenska"},
            {"code": "da", "name": "Danish", "native": "Dansk"},
            {"code": "no", "name": "Norwegian", "native": "Norsk"},
            {"code": "fi", "name": "Finnish", "native": "Suomi"},
            {"code": "cs", "name": "Czech", "native": "Čeština"},
            {"code": "hu", "name": "Hungarian", "native": "Magyar"},
            {"code": "ro", "name": "Romanian", "native": "Română"},
            {"code": "bg", "name": "Bulgarian", "native": "Български"},
            {"code": "hr", "name": "Croatian", "native": "Hrvatski"},
            {"code": "sk", "name": "Slovak", "native": "Slovenčina"},
            {"code": "sl", "name": "Slovenian", "native": "Slovenščina"},
            {"code": "et", "name": "Estonian", "native": "Eesti"},
            {"code": "lv", "name": "Latvian", "native": "Latviešu"},
            {"code": "lt", "name": "Lithuanian", "native": "Lietuvių"},
            {"code": "mt", "name": "Maltese", "native": "Malti"},
            {"code": "el", "name": "Greek", "native": "Ελληνικά"},
            {"code": "he", "name": "Hebrew", "native": "עברית"},
            {"code": "th", "name": "Thai", "native": "ไทย"},
            {"code": "vi", "name": "Vietnamese", "native": "Tiếng Việt"},
            {"code": "id", "name": "Indonesian", "native": "Bahasa Indonesia"},
            {"code": "ms", "name": "Malay", "native": "Bahasa Melayu"},
            {"code": "tl", "name": "Filipino", "native": "Filipino"},
            {"code": "bn", "name": "Bengali", "native": "বাংলা"},
            {"code": "ta", "name": "Tamil", "native": "தமிழ்"},
            {"code": "te", "name": "Telugu", "native": "తెలుగు"},
            {"code": "kn", "name": "Kannada", "native": "ಕನ್ನಡ"},
            {"code": "ml", "name": "Malayalam", "native": "മലയാളം"},
            {"code": "gu", "name": "Gujarati", "native": "ગુજરાતી"},
            {"code": "pa", "name": "Punjabi", "native": "ਪੰਜਾਬੀ"},
            {"code": "or", "name": "Odia", "native": "ଓଡ଼ିଆ"},
            {"code": "as", "name": "Assamese", "native": "অসমীয়া"},
            {"code": "ne", "name": "Nepali", "native": "नेपाली"},
            {"code": "si", "name": "Sinhala", "native": "සිංහල"},
            {"code": "my", "name": "Burmese", "native": "မြန်မာ"},
            {"code": "km", "name": "Khmer", "native": "ខ្មែរ"},
            {"code": "lo", "name": "Lao", "native": "ລາວ"},
            {"code": "ka", "name": "Georgian", "native": "ქართული"},
            {"code": "am", "name": "Amharic", "native": "አማርኛ"},
            {"code": "sw", "name": "Swahili", "native": "Kiswahili"},
            {"code": "zu", "name": "Zulu", "native": "isiZulu"},
            {"code": "af", "name": "Afrikaans", "native": "Afrikaans"},
            {"code": "is", "name": "Icelandic", "native": "Íslenska"},
            {"code": "fo", "name": "Faroese", "native": "Føroyskt"},
            {"code": "cy", "name": "Welsh", "native": "Cymraeg"},
            {"code": "ga", "name": "Irish", "native": "Gaeilge"},
            {"code": "gd", "name": "Scottish Gaelic", "native": "Gàidhlig"},
            {"code": "kw", "name": "Cornish", "native": "Kernewek"},
            {"code": "br", "name": "Breton", "native": "Brezhoneg"},
            {"code": "eu", "name": "Basque", "native": "Euskara"},
            {"code": "ca", "name": "Catalan", "native": "Català"},
            {"code": "gl", "name": "Galician", "native": "Galego"},
            {"code": "oc", "name": "Occitan", "native": "Occitan"},
            {"code": "rm", "name": "Romansh", "native": "Rumantsch"},
            {"code": "fur", "name": "Friulian", "native": "Furlan"},
            {"code": "sc", "name": "Sardinian", "native": "Sardu"},
            {"code": "vec", "name": "Venetian", "native": "Vèneto"},
            {"code": "lmo", "name": "Lombard", "native": "Lombard"},
            {"code": "pms", "name": "Piedmontese", "native": "Piemontèis"},
            {"code": "nap", "name": "Neapolitan", "native": "Nnapulitano"},
            {"code": "scn", "name": "Sicilian", "native": "Sicilianu"},
            {"code": "co", "name": "Corsican", "native": "Corsu"},
            {"code": "lij", "name": "Ligurian", "native": "Lìgure"},
            {"code": "eml", "name": "Emilian", "native": "Emiliàn"},
            {"code": "rgn", "name": "Romagnol", "native": "Rumagnòl"},
            {"code": "pms", "name": "Piedmontese", "native": "Piemontèis"},
            {"code": "lmo", "name": "Lombard", "native": "Lombard"},
            {"code": "vec", "name": "Venetian", "native": "Vèneto"},
            {"code": "fur", "name": "Friulian", "native": "Furlan"},
            {"code": "sc", "name": "Sardinian", "native": "Sardu"},
            {"code": "co", "name": "Corsican", "native": "Corsu"},
            {"code": "lij", "name": "Ligurian", "native": "Lìgure"},
            {"code": "eml", "name": "Emilian", "native": "Emiliàn"},
            {"code": "rgn", "name": "Romagnol", "native": "Rumagnòl"}
        ]


# Global service instance
_whisper_service = None


def get_whisper_service() -> WhisperService:
    """Get or create the global Whisper service instance."""
    global _whisper_service
    if _whisper_service is None:
        _whisper_service = WhisperService()
    return _whisper_service


def transcribe_audio_file(audio_file_path: str, language: Optional[str] = None, 
                         include_timestamps: bool = False) -> Dict[str, Any]:
    """
    Transcribe an audio file using the Whisper service.
    
    Args:
        audio_file_path: Path to the audio file
        language: Language hint for transcription
        include_timestamps: Whether to include timestamps
        
    Returns:
        Transcription results
    """
    service = get_whisper_service()
    return service.transcribe_audio(audio_file_path, language, include_timestamps)


def get_supported_languages() -> list:
    """Get list of supported languages."""
    service = get_whisper_service()
    return service.get_supported_languages()


# Export commonly used items
SUPPORTED_LANGUAGES = get_supported_languages() if 'get_supported_languages' in globals() else []
