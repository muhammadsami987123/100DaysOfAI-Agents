#!/usr/bin/env python3
"""
Test script for SocialPostCreatorAgent
Verifies installation and basic functionality
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import openai
        print("✅ OpenAI package imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI package import failed: {e}")
        return False
    
    try:
        import rich
        print("✅ Rich package imported successfully")
    except ImportError as e:
        print(f"❌ Rich package import failed: {e}")
        return False
    
    try:
        import flask
        print("✅ Flask package imported successfully")
    except ImportError as e:
        print(f"❌ Flask package import failed: {e}")
        return False
    
    try:
        import pyperclip
        print("✅ Pyperclip package imported successfully")
    except ImportError as e:
        print(f"❌ Pyperclip package import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests package imported successfully")
    except ImportError as e:
        print(f"❌ Requests package import failed: {e}")
        return False
    
    return True


def test_config():
    """Test if configuration can be loaded"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import Config
        print("✅ Configuration loaded successfully")
        
        # Check platform limits
        platforms = list(Config.PLATFORM_LIMITS.keys())
        print(f"✅ Supported platforms: {', '.join(platforms)}")
        
        # Check OpenAI API key
        if Config.OPENAI_API_KEY:
            print("✅ OpenAI API key is set")
        else:
            print("⚠️  OpenAI API key is not set (set OPENAI_API_KEY in .env)")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False


def test_ai_service():
    """Test if AI service can be imported and configured"""
    print("\n🤖 Testing AI service...")
    
    try:
        from ai_service import generate_social_post, generate_tweet
        print("✅ AI service imported successfully")
        
        # Test if we can create the OpenAI client (without making API calls)
        try:
            from ai_service import _ensure_openai
            client = _ensure_openai()
            print("✅ OpenAI client can be created")
        except RuntimeError as e:
            if "OPENAI_API_KEY is not set" in str(e):
                print("⚠️  OpenAI client creation failed: API key not set (expected)")
            else:
                print(f"❌ OpenAI client creation failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ AI service import failed: {e}")
        return False


def test_search_service():
    """Test if search service can be imported"""
    print("\n🔍 Testing search service...")
    
    try:
        from search_service import fetch_latest_insights
        print("✅ Search service imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Search service import failed: {e}")
        return False


def test_poster_service():
    """Test if poster service can be imported"""
    print("\n📝 Testing poster service...")
    
    try:
        from poster import save_post_to_file, save_tweet_to_file
        print("✅ Poster service imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Poster service import failed: {e}")
        return False


def test_web_app():
    """Test if web app can be imported"""
    print("\n🌐 Testing web app...")
    
    try:
        from web_app import app
        print("✅ Web app imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Web app import failed: {e}")
        return False


def test_cli():
    """Test if CLI can be imported"""
    print("\n💻 Testing CLI...")
    
    try:
        from cli import main, get_available_platforms, get_available_tones
        print("✅ CLI imported successfully")
        
        # Test helper functions
        platforms = get_available_platforms()
        tones = get_available_tones()
        print(f"✅ Available platforms: {len(platforms)}")
        print(f"✅ Available tones: {len(tones)}")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI import failed: {e}")
        return False


def test_directory_structure():
    """Test if required directories and files exist"""
    print("\n📁 Testing directory structure...")
    
    required_files = [
        "config.py",
        "ai_service.py",
        "search_service.py",
        "poster.py",
        "cli.py",
        "web_app.py",
        "requirements.txt",
        "README.md"
    ]
    
    required_dirs = [
        "templates",
        "static/js"
    ]
    
    all_good = True
    
    # Check required files
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_good = False
    
    # Check required directories
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/ directory exists")
        else:
            print(f"❌ {dir_path}/ directory missing")
            all_good = False
    
    return all_good


def test_environment():
    """Test environment setup"""
    print("\n🌍 Testing environment...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 8:
        print(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"❌ Python version {python_version.major}.{python_version.minor} is too old. Need 3.8+")
        return False
    
    # Check if we're in the right directory
    current_dir = Path.cwd().name
    if "SocialPostCreatorAgent" in current_dir:
        print(f"✅ Current directory: {current_dir}")
    else:
        print(f"⚠️  Current directory: {current_dir} (expected to contain 'SocialPostCreatorAgent')")
    
    return True


def main():
    """Run all tests"""
    print("🚀 SocialPostCreatorAgent - Installation Test")
    print("=" * 50)
    
    tests = [
        test_environment,
        test_imports,
        test_config,
        test_ai_service,
        test_search_service,
        test_poster_service,
        test_web_app,
        test_cli,
        test_directory_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! SocialPostCreatorAgent is ready to use.")
        print("\n🚀 Quick start:")
        print("1. Set your OPENAI_API_KEY in .env file")
        print("2. Run: python -m 22_SocialPostCreatorAgent.cli")
        print("3. Or run: python -m 22_SocialPostCreatorAgent.web_app")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
