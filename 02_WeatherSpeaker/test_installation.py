#!/usr/bin/env python3
"""
Test script to verify Weather Speaker Agent installation
"""

import sys
import importlib
import os

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'openai',
        'requests',
        'python-multipart',
        'pyttsx3',
        'gtts',
        'python-dotenv',
        'aiofiles',
        'jinja2'
    ]
    
    print("🔍 Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    return failed_imports

def test_config():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    try:
        from config import Config
        print("✅ Configuration module imported")
        
        # Test if OpenAI key is set (don't validate it here)
        if Config.OPENAI_API_KEY:
            print("✅ OpenAI API key found")
        else:
            print("⚠️  OpenAI API key not found (set OPENAI_API_KEY in .env file)")
            
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_services():
    """Test service modules"""
    print("\n🛠️  Testing service modules...")
    
    try:
        from weather_service import WeatherService
        print("✅ Weather service imported")
    except Exception as e:
        print(f"❌ Weather service error: {e}")
        return False
    
    try:
        from tts_service import TTSService
        print("✅ TTS service imported")
    except Exception as e:
        print(f"❌ TTS service error: {e}")
        return False
    
    try:
        from ai_agent import WeatherAgent
        print("✅ AI agent imported")
    except Exception as e:
        print(f"❌ AI agent error: {e}")
        return False
    
    return True

def test_fastapi():
    """Test FastAPI application"""
    print("\n🚀 Testing FastAPI application...")
    try:
        from main import app
        print("✅ FastAPI app imported")
        print(f"✅ App title: {app.title}")
        return True
    except Exception as e:
        print(f"❌ FastAPI error: {e}")
        return False

def main():
    """Run all tests"""
    print("🌤️ Weather Speaker Agent - Installation Test")
    print("=" * 50)
    
    # Test Python version
    print(f"🐍 Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print("✅ Python version OK")
    
    # Test imports
    failed_imports = test_imports()
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    # Test configuration
    if not test_config():
        return False
    
    # Test services
    if not test_services():
        return False
    
    # Test FastAPI
    if not test_fastapi():
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Weather Speaker Agent is ready to run.")
    print("\n📋 Next steps:")
    print("1. Set your OPENAI_API_KEY in .env file")
    print("2. Run: python main.py")
    print("3. Open: http://localhost:8000")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 