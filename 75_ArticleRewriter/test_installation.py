#!/usr/bin/env python3
"""
Test script to verify ArticleRewriter installation
"""

import sys
import importlib
import os
from pathlib import Path

def test_python_version():
    """Test if Python version is compatible"""
    print("🐍 Testing Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - OK")
        return True

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'openai',
        'google.generativeai',
        'dotenv',
        'jinja2',
        'multipart'
    ]
    
    print("\n🔍 Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    return failed_imports

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")
    required_files = [
        'main.py',
        'config.py',
        'agents/article_rewriter_agent.py',
        'templates/index.html',
        'static/js/app.js',
        'prompts/tone_prompt.txt',
        'requirements.txt'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ Missing: {file_path}")
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    return missing_files

def test_config():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    try:
        from config import Config
        print("✅ Configuration module imported")
        
        # Test tone configuration
        tones = Config.get_available_tones()
        if tones and len(tones) > 0:
            print(f"✅ Tones configured: {len(tones)} available")
        else:
            print("❌ No tones configured")
            return False
        
        # Test language configuration
        languages = Config.get_available_languages()
        if languages and len(languages) > 0:
            print(f"✅ Languages configured: {len(languages)} available")
        else:
            print("❌ No languages configured")
            return False
        
        # Test API keys
        if Config.LLM_MODEL.lower() == "gemini":
            if Config.GEMINI_API_KEY:
                print("✅ Gemini API key found")
            else:
                print("⚠️  Gemini API key not found (set GEMINI_API_KEY in .env file)")
        elif Config.LLM_MODEL.lower() == "openai":
            if Config.OPENAI_API_KEY:
                print("✅ OpenAI API key found")
            else:
                print("⚠️  OpenAI API key not found (set OPENAI_API_KEY in .env file)")
        else:
            print("⚠️  No valid LLM model configured")
        
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_article_rewriter_agent():
    """Test ArticleRewriterAgent initialization"""
    print("\n🤖 Testing ArticleRewriterAgent...")
    try:
        from agents.article_rewriter_agent import ArticleRewriterAgent
        print("✅ ArticleRewriterAgent module imported")
        
        # Test agent initialization
        agent = ArticleRewriterAgent()
        print("✅ ArticleRewriterAgent initialized")
        
        # Test available tones
        tones = agent.get_available_tones()
        if tones:
            print(f"✅ Available tones: {list(tones.keys())}")
        else:
            print("❌ No tones available")
            return False
        
        # Test available languages
        languages = agent.get_available_languages()
        if languages:
            print(f"✅ Available languages: {list(languages.keys())}")
        else:
            print("❌ No languages available")
            return False
        
        return True
    except Exception as e:
        print(f"❌ ArticleRewriterAgent error: {e}")
        return False

def test_web_app():
    """Test FastAPI application"""
    print("\n🚀 Testing FastAPI application...")
    try:
        from main import app
        print("✅ FastAPI app imported")
        print(f"✅ App title: {app.title}")
        print(f"✅ App version: {app.version}")
        return True
    except Exception as e:
        print(f"❌ FastAPI error: {e}")
        return False

def test_directories():
    """Test if required directories exist"""
    print("\n📂 Testing directories...")
    required_dirs = [
        'agents',
        'templates',
        'static',
        'static/css',
        'static/js',
        'prompts',
        'outputs'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            print(f"❌ Missing directory: {dir_path}")
            missing_dirs.append(dir_path)
        else:
            print(f"✅ {dir_path}")
    
    return missing_dirs

def main():
    """Run all tests"""
    print("📝 ArticleRewriter - Installation Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test Python version
    if not test_python_version():
        all_tests_passed = False
    
    # Test imports
    failed_imports = test_imports()
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("💡 Run: pip install -r requirements.txt")
        all_tests_passed = False
    
    # Test file structure
    missing_files = test_file_structure()
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        all_tests_passed = False
    
    # Test configuration
    if not test_config():
        all_tests_passed = False
    
    # Test directories
    missing_dirs = test_directories()
    if missing_dirs:
        print(f"\n❌ Missing directories: {', '.join(missing_dirs)}")
        all_tests_passed = False
    
    # Test ArticleRewriterAgent
    if not test_article_rewriter_agent():
        all_tests_passed = False
    
    # Test web app
    if not test_web_app():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! ArticleRewriter is ready to run.")
        print("\n📋 Next steps:")
        print("1. Set your OpenAI API key in .env file")
        print("2. Run: python main.py")
        print("3. Open: http://localhost:8075")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
