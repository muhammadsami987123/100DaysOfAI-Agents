import openai
import json
import logging
from typing import Dict, List, Optional, Tuple
from config import TranslatorConfig, TRANSLATION_PROMPTS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranslatorAgent:
    """AI-powered translation agent using OpenAI GPT"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the TranslatorAgent"""
        self.api_key = api_key or TranslatorConfig.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = TranslatorConfig.OPENAI_MODEL
        self.max_tokens = TranslatorConfig.MAX_TOKENS
        self.temperature = TranslatorConfig.TEMPERATURE
        
        # Translation history
        self.history: List[Dict] = []
    
    def translate_text(
        self, 
        text: str, 
        source_lang: str = "auto", 
        target_lang: str = "en",
        style: str = "general"
    ) -> Dict:
        """
        Translate text using AI
        
        Args:
            text: Text to translate
            source_lang: Source language code (or 'auto' for detection)
            target_lang: Target language code
            style: Translation style (general, formal, casual, technical, literary)
        
        Returns:
            Dictionary containing translation results
        """
        try:
            # Validate languages
            if source_lang != "auto" and not TranslatorConfig.is_supported(source_lang):
                raise ValueError(f"Unsupported source language: {source_lang}")
            
            if not TranslatorConfig.is_supported(target_lang):
                raise ValueError(f"Unsupported target language: {target_lang}")
            
            # Detect source language if needed
            if source_lang == "auto":
                detected_lang = self._detect_language(text)
                source_lang = detected_lang
                logger.info(f"Detected language: {source_lang}")
            
            # Get language names
            source_name = TranslatorConfig.get_language_name(source_lang)
            target_name = TranslatorConfig.get_language_name(target_lang)
            
            # Create translation prompt
            prompt = self._create_translation_prompt(
                text, source_name, target_name, style
            )
            
            # Get AI translation
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional translator. Provide accurate, natural translations that preserve the original meaning and tone."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            translation = response.choices[0].message.content.strip()
            
            # Create result
            result = {
                "success": True,
                "original_text": text,
                "translation": translation,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "source_name": source_name,
                "target_name": target_name,
                "confidence": 0.95,  # AI confidence
                "style": style
            }
            
            # Add to history
            self._add_to_history(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "original_text": text,
                "source_lang": source_lang,
                "target_lang": target_lang
            }
    
    def detect_language(self, text: str) -> Dict:
        """
        Detect the language of the given text
        
        Args:
            text: Text to analyze
        
        Returns:
            Dictionary containing detection results
        """
        try:
            prompt = f"""Detect the language of the following text and respond with only the ISO 639-1 language code (e.g., 'en', 'es', 'fr'):

Text: "{text}"

Language code:"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a language detection expert. Respond with only the ISO 639-1 language code."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=10,
                temperature=0.1
            )
            
            detected_lang = response.choices[0].message.content.strip().lower()
            
            # Validate detected language
            if not TranslatorConfig.is_supported(detected_lang):
                detected_lang = "en"  # Fallback to English
            
            return {
                "success": True,
                "text": text,
                "detected_language": detected_lang,
                "language_name": TranslatorConfig.get_language_name(detected_lang),
                "confidence": 0.9
            }
            
        except Exception as e:
            logger.error(f"Language detection error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "text": text
            }
    
    def get_pronunciation(self, text: str, language: str) -> str:
        """
        Get pronunciation guide for translated text
        
        Args:
            text: Text to get pronunciation for
            language: Language code
        
        Returns:
            Pronunciation guide
        """
        try:
            prompt = f"""Provide a pronunciation guide for the following text in {TranslatorConfig.get_language_name(language)}. 
            Use IPA (International Phonetic Alphabet) or a simple phonetic guide that's easy to read:

Text: "{text}"

Pronunciation:"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a pronunciation expert. Provide clear, easy-to-read pronunciation guides."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Pronunciation error: {str(e)}")
            return text  # Return original text if pronunciation fails
    
    def batch_translate(
        self, 
        texts: List[str], 
        source_lang: str = "auto", 
        target_lang: str = "en"
    ) -> List[Dict]:
        """
        Translate multiple texts at once
        
        Args:
            texts: List of texts to translate
            source_lang: Source language code
            target_lang: Target language code
        
        Returns:
            List of translation results
        """
        results = []
        for text in texts:
            result = self.translate_text(text, source_lang, target_lang)
            results.append(result)
        return results
    
    def get_supported_languages(self) -> List[Dict]:
        """Get list of supported languages"""
        return TranslatorConfig.get_language_list()
    
    def get_translation_history(self) -> List[Dict]:
        """Get translation history"""
        return self.history
    
    def clear_history(self) -> None:
        """Clear translation history"""
        self.history = []
    
    def _create_translation_prompt(
        self, 
        text: str, 
        source_lang: str, 
        target_lang: str, 
        style: str
    ) -> str:
        """Create translation prompt based on style"""
        base_prompt = TRANSLATION_PROMPTS.get(style, TRANSLATION_PROMPTS["general"])
        prompt = base_prompt.format(source_lang=source_lang, target_lang=target_lang)
        
        return f"{prompt}\n\nText: {text}\n\nTranslation:"
    
    def _detect_language(self, text: str) -> str:
        """Detect language of text"""
        result = self.detect_language(text)
        if result["success"]:
            return result["detected_language"]
        return "en"  # Fallback to English
    
    def _add_to_history(self, translation_result: Dict) -> None:
        """Add translation to history"""
        history_entry = {
            "timestamp": self._get_timestamp(),
            "original_text": translation_result["original_text"],
            "translation": translation_result["translation"],
            "source_lang": translation_result["source_lang"],
            "target_lang": translation_result["target_lang"],
            "style": translation_result.get("style", "general")
        }
        
        self.history.append(history_entry)
        
        # Keep only last 50 translations
        if len(self.history) > 50:
            self.history = self.history[-50:]
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def health_check(self) -> Dict:
        """Check if the translator is working properly"""
        try:
            # Test with a simple translation
            test_result = self.translate_text("Hello", "en", "es")
            return {
                "status": "healthy",
                "api_key_valid": True,
                "model_available": True,
                "test_translation": test_result["success"]
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "api_key_valid": bool(self.api_key),
                "model_available": False,
                "test_translation": False
            } 