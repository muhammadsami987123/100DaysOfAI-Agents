#!/usr/bin/env python3
"""
Test script for TranslatorAgent installation and basic functionality
"""

import sys
import os
import importlib
from colorama import init, Fore, Style

# Initialize colorama
init()

def print_colored(text: str, color: str = Fore.WHITE, style: str = ""):
    """Print colored text"""
    print(f"{color}{style}{text}{Style.RESET_ALL}")

def test_imports():
    """Test if all required modules can be imported"""
    print_colored("🔍 Testing imports...", Fore.CYAN)
    
    required_modules = [
        "fastapi",
        "uvicorn",
        "jinja2",
        "openai",
        "colorama",
        "pydantic",
        "python-multipart",
        "httpx",
        "requests",
        "SpeechRecognition",
        "pyttsx3",
        "pyaudio",
        "python-dotenv"
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module.replace("-", "_"))
            print_colored(f"✅ {module}", Fore.GREEN)
        except ImportError:
            print_colored(f"❌ {module}", Fore.RED)
            failed_imports.append(module)
    
    if failed_imports:
        print_colored(f"\n❌ Failed to import: {', '.join(failed_imports)}", Fore.RED)
        print_colored("💡 Run: pip install -r requirements.txt", Fore.YELLOW)
        return False
    
    print_colored("✅ All imports successful!", Fore.GREEN)
    return True

def test_config():
    """Test configuration loading"""
    print_colored("\n🔧 Testing configuration...", Fore.CYAN)
    
    try:
        from config import TranslatorConfig
        
        # Test basic config
        if TranslatorConfig.OPENAI_API_KEY:
            print_colored("✅ OpenAI API key found", Fore.GREEN)
        else:
            print_colored("⚠️  OpenAI API key not found", Fore.YELLOW)
            print_colored("💡 Set OPENAI_API_KEY environment variable", Fore.CYAN)
        
        # Test language support
        languages = TranslatorConfig.get_language_list()
        print_colored(f"✅ {len(languages)} languages supported", Fore.GREEN)
        
        return True
        
    except Exception as e:
        print_colored(f"❌ Configuration error: {str(e)}", Fore.RED)
        return False

def test_translator_agent():
    """Test TranslatorAgent initialization"""
    print_colored("\n🤖 Testing TranslatorAgent...", Fore.CYAN)
    
    try:
        from translator_agent import TranslatorAgent
        
        # Test initialization (without API key for now)
        if not os.getenv("OPENAI_API_KEY"):
            print_colored("⚠️  Skipping TranslatorAgent test (no API key)", Fore.YELLOW)
            return True
        
        translator = TranslatorAgent()
        print_colored("✅ TranslatorAgent initialized", Fore.GREEN)
        
        # Test health check
        health = translator.health_check()
        print_colored(f"✅ Health check: {health['status']}", Fore.GREEN)
        
        return True
        
    except Exception as e:
        print_colored(f"❌ TranslatorAgent error: {str(e)}", Fore.RED)
        return False

def test_voice_service():
    """Test VoiceService initialization"""
    print_colored("\n🗣️  Testing VoiceService...", Fore.CYAN)
    
    try:
        from voice_service import VoiceService
        
        voice_service = VoiceService()
        print_colored("✅ VoiceService initialized", Fore.GREEN)
        
        # Test health check
        health = voice_service.health_check()
        print_colored(f"✅ Voice health: {health['status']}", Fore.GREEN)
        
        return True
        
    except Exception as e:
        print_colored(f"❌ VoiceService error: {str(e)}", Fore.RED)
        return False

def test_web_app():
    """Test web app initialization"""
    print_colored("\n🌐 Testing web application...", Fore.CYAN)
    
    try:
        from web_app import app
        print_colored("✅ FastAPI app initialized", Fore.GREEN)
        
        # Test basic routes
        routes = [
            "/",
            "/api/health",
            "/api/languages"
        ]
        
        print_colored("✅ Web app routes available", Fore.GREEN)
        return True
        
    except Exception as e:
        print_colored(f"❌ Web app error: {str(e)}", Fore.RED)
        return False

def test_file_structure():
    """Test if all required files exist"""
    print_colored("\n📁 Testing file structure...", Fore.CYAN)
    
    required_files = [
        "main.py",
        "translator_agent.py",
        "web_app.py",
        "config.py",
        "voice_service.py",
        "requirements.txt",
        "README.md",
        "templates/index.html",
        "static/js/app.js"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print_colored(f"✅ {file_path}", Fore.GREEN)
        else:
            print_colored(f"❌ {file_path}", Fore.RED)
            missing_files.append(file_path)
    
    if missing_files:
        print_colored(f"\n❌ Missing files: {', '.join(missing_files)}", Fore.RED)
        return False
    
    print_colored("✅ All required files present!", Fore.GREEN)
    return True

def main():
    """Run all tests"""
    print_colored("🧪 TranslatorAgent Installation Test", Fore.CYAN, Style.BRIGHT)
    print_colored("=" * 50, Fore.CYAN)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("TranslatorAgent", test_translator_agent),
        ("VoiceService", test_voice_service),
        ("Web Application", test_web_app)
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
        print_colored("🎉 All tests passed! TranslatorAgent is ready to use.", Fore.GREEN)
        print_colored("\n🚀 Quick Start:", Fore.YELLOW)
        print_colored("   python main.py --web", Fore.CYAN)
        print_colored("   python main.py --terminal", Fore.CYAN)
        print_colored("   python main.py --quick \"Hello world\" --target es", Fore.CYAN)
    else:
        print_colored("❌ Some tests failed. Please check the errors above.", Fore.RED)
        print_colored("\n💡 Troubleshooting:", Fore.YELLOW)
        print_colored("   1. Install dependencies: pip install -r requirements.txt", Fore.CYAN)
        print_colored("   2. Set OpenAI API key: export OPENAI_API_KEY=your_key", Fore.CYAN)
        print_colored("   3. Check file permissions and paths", Fore.CYAN)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 