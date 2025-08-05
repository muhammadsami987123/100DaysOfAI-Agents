#!/usr/bin/env python3
"""
Test script for TranslatorAgent translation functionality
"""

import sys
import os
from colorama import init, Fore, Style

# Initialize colorama
init()

def print_colored(text: str, color: str = Fore.WHITE, style: str = ""):
    """Print colored text"""
    print(f"{color}{style}{text}{Style.RESET_ALL}")

def test_basic_translation():
    """Test basic translation functionality"""
    print_colored("🔄 Testing basic translation...", Fore.CYAN)
    
    try:
        from translator_agent import TranslatorAgent
        
        if not os.getenv("OPENAI_API_KEY"):
            print_colored("❌ OpenAI API key required for translation tests", Fore.RED)
            return False
        
        translator = TranslatorAgent()
        
        # Test cases
        test_cases = [
            {
                "text": "Hello, how are you?",
                "source": "en",
                "target": "es",
                "expected_lang": "Spanish"
            },
            {
                "text": "Bonjour le monde",
                "source": "fr",
                "target": "en",
                "expected_lang": "English"
            },
            {
                "text": "Hola mundo",
                "source": "auto",
                "target": "en",
                "expected_lang": "English"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print_colored(f"\n📝 Test {i}: {test_case['text']}", Fore.YELLOW)
            
            result = translator.translate_text(
                text=test_case['text'],
                source_lang=test_case['source'],
                target_lang=test_case['target']
            )
            
            if result["success"]:
                print_colored(f"✅ Translation: {result['translation']}", Fore.GREEN)
                print_colored(f"   From: {result['source_name']} → To: {result['target_name']}", Fore.CYAN)
            else:
                print_colored(f"❌ Translation failed: {result['error']}", Fore.RED)
                return False
        
        return True
        
    except Exception as e:
        print_colored(f"❌ Translation test error: {str(e)}", Fore.RED)
        return False

def test_language_detection():
    """Test language detection functionality"""
    print_colored("\n🔍 Testing language detection...", Fore.CYAN)
    
    try:
        from translator_agent import TranslatorAgent
        
        if not os.getenv("OPENAI_API_KEY"):
            print_colored("❌ OpenAI API key required for detection tests", Fore.RED)
            return False
        
        translator = TranslatorAgent()
        
        # Test cases
        test_cases = [
            "Hello world",
            "Bonjour le monde",
            "Hola mundo",
            "こんにちは世界",
            "Привет мир"
        ]
        
        for text in test_cases:
            print_colored(f"\n🔍 Detecting: {text}", Fore.YELLOW)
            
            result = translator.detect_language(text)
            
            if result["success"]:
                print_colored(f"✅ Detected: {result['language_name']} ({result['detected_language']})", Fore.GREEN)
                print_colored(f"   Confidence: {result['confidence']:.2f}", Fore.CYAN)
            else:
                print_colored(f"❌ Detection failed: {result['error']}", Fore.RED)
                return False
        
        return True
        
    except Exception as e:
        print_colored(f"❌ Detection test error: {str(e)}", Fore.RED)
        return False

def test_pronunciation():
    """Test pronunciation functionality"""
    print_colored("\n🗣️  Testing pronunciation...", Fore.CYAN)
    
    try:
        from translator_agent import TranslatorAgent
        
        if not os.getenv("OPENAI_API_KEY"):
            print_colored("❌ OpenAI API key required for pronunciation tests", Fore.RED)
            return False
        
        translator = TranslatorAgent()
        
        # Test cases
        test_cases = [
            ("Hello world", "en"),
            ("Hola mundo", "es"),
            ("Bonjour le monde", "fr")
        ]
        
        for text, lang in test_cases:
            print_colored(f"\n🗣️  Pronunciation: {text} ({lang})", Fore.YELLOW)
            
            pronunciation = translator.get_pronunciation(text, lang)
            
            if pronunciation and pronunciation != text:
                print_colored(f"✅ Pronunciation: {pronunciation}", Fore.GREEN)
            else:
                print_colored(f"⚠️  No pronunciation guide available", Fore.YELLOW)
        
        return True
        
    except Exception as e:
        print_colored(f"❌ Pronunciation test error: {str(e)}", Fore.RED)
        return False

def test_voice_features():
    """Test voice features"""
    print_colored("\n🎤 Testing voice features...", Fore.CYAN)
    
    try:
        from voice_service import VoiceService
        
        voice_service = VoiceService()
        
        # Test health check
        health = voice_service.health_check()
        print_colored(f"✅ Voice health: {health['status']}", Fore.GREEN)
        
        if health['tts_available']:
            print_colored("✅ Text-to-speech available", Fore.GREEN)
        else:
            print_colored("⚠️  Text-to-speech not available", Fore.YELLOW)
        
        if health['microphone_available']:
            print_colored("✅ Microphone available", Fore.GREEN)
        else:
            print_colored("⚠️  Microphone not available", Fore.YELLOW)
        
        return True
        
    except Exception as e:
        print_colored(f"❌ Voice test error: {str(e)}", Fore.RED)
        return False

def test_supported_languages():
    """Test supported languages"""
    print_colored("\n🌍 Testing supported languages...", Fore.CYAN)
    
    try:
        from config import TranslatorConfig
        
        languages = TranslatorConfig.get_language_list()
        print_colored(f"✅ {len(languages)} languages supported", Fore.GREEN)
        
        # Show some popular languages
        popular_langs = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh']
        
        print_colored("\n📋 Popular Languages:", Fore.CYAN)
        for lang_code in popular_langs:
            if TranslatorConfig.is_supported(lang_code):
                name = TranslatorConfig.get_language_name(lang_code)
                native = TranslatorConfig.get_native_name(lang_code)
                print_colored(f"   {lang_code}: {name} ({native})", Fore.GREEN)
            else:
                print_colored(f"   {lang_code}: Not supported", Fore.RED)
        
        return True
        
    except Exception as e:
        print_colored(f"❌ Language test error: {str(e)}", Fore.RED)
        return False

def main():
    """Run all translation tests"""
    print_colored("🧪 TranslatorAgent Translation Tests", Fore.CYAN, Style.BRIGHT)
    print_colored("=" * 50, Fore.CYAN)
    
    tests = [
        ("Supported Languages", test_supported_languages),
        ("Voice Features", test_voice_features),
        ("Language Detection", test_language_detection),
        ("Basic Translation", test_basic_translation),
        ("Pronunciation", test_pronunciation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print_colored(f"❌ {test_name} failed with exception: {str(e)}", Fore.RED)
    
    print_colored("\n" + "=" * 50, Fore.CYAN)
    print_colored(f"📊 Test Results: {passed}/{total} passed", Fore.CYAN)
    
    if passed == total:
        print_colored("🎉 All translation tests passed!", Fore.GREEN)
        print_colored("\n🚀 Ready for translation:", Fore.YELLOW)
        print_colored("   python main.py --web", Fore.CYAN)
        print_colored("   python main.py --quick \"Hello world\" --target es", Fore.CYAN)
    else:
        print_colored("❌ Some tests failed. Please check the errors above.", Fore.RED)
        print_colored("\n💡 Make sure you have:", Fore.YELLOW)
        print_colored("   1. OpenAI API key set", Fore.CYAN)
        print_colored("   2. All dependencies installed", Fore.CYAN)
        print_colored("   3. Microphone permissions (for voice tests)", Fore.CYAN)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 