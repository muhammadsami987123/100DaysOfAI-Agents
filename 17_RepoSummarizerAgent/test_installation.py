#!/usr/bin/env python3
"""
Test script for RepoSummarizerAgent - Day 17 of #100DaysOfAI-Agents

This script tests the basic installation and functionality of the agent.
"""

import sys
import os
from pathlib import Path


def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing module imports...")
    
    try:
        from config import validate_config, get_language_config
        print("✅ Config module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import config module: {e}")
        return False
    
    try:
        from github_service import GitHubService
        print("✅ GitHub service module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import GitHub service module: {e}")
        return False
    
    try:
        from ai_summarizer import AISummarizer
        print("✅ AI summarizer module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import AI summarizer module: {e}")
        return False
    
    return True


def test_config():
    """Test configuration validation."""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import validate_config, get_language_config, SUPPORTED_LANGUAGES
        
        # Test language configuration
        en_config = get_language_config("en")
        if en_config["code"] == "en":
            print("✅ Language configuration working")
        else:
            print("❌ Language configuration failed")
            return False
        
        # Test supported languages
        if len(SUPPORTED_LANGUAGES) >= 3:  # en, hi, ur
            print("✅ Supported languages configuration complete")
        else:
            print("❌ Supported languages configuration incomplete")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_github_service():
    """Test GitHub service initialization."""
    print("\n🌐 Testing GitHub service...")
    
    try:
        from github_service import GitHubService
        
        service = GitHubService()
        print("✅ GitHub service initialized successfully")
        
        # Test URL parsing
        test_url = "https://github.com/user/repo"
        parsed = service.parse_github_url(test_url)
        if parsed and len(parsed) == 2:
            print("✅ GitHub URL parsing working")
        else:
            print("❌ GitHub URL parsing failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ GitHub service test failed: {e}")
        return False


def test_ai_summarizer():
    """Test AI summarizer initialization."""
    print("\n🤖 Testing AI summarizer...")
    
    try:
        from ai_summarizer import AISummarizer
        
        # This will fail without API key, but we can test the class structure
        try:
            summarizer = AISummarizer()
            print("✅ AI summarizer initialized successfully")
        except ValueError as e:
            if "OpenAI API key is required" in str(e):
                print("✅ AI summarizer validation working (API key required)")
            else:
                print(f"❌ AI summarizer validation failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ AI summarizer test failed: {e}")
        return False


def test_file_structure():
    """Test if all required files exist."""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "config.py",
        "github_service.py", 
        "ai_summarizer.py",
        "main.py",
        "requirements.txt",
        "install.bat",
        "start.bat",
        "setup.py"
    ]
    
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present")
    return True


def test_dependencies():
    """Test if required packages are installed."""
    print("\n📦 Testing dependencies...")
    
    required_packages = [
        "openai",
        "requests", 
        "python-dotenv"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages installed")
    return True


def main():
    """Run all tests."""
    print("🚀 RepoSummarizerAgent - Day 17 Installation Test")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Dependencies", test_dependencies),
        ("Module Imports", test_imports),
        ("Configuration", test_config),
        ("GitHub Service", test_github_service),
        ("AI Summarizer", test_ai_summarizer)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! RepoSummarizerAgent is ready to use.")
        print("\nNext steps:")
        print("1. Set up your .env file with OpenAI API key")
        print("2. Run: python main.py --url https://github.com/user/repo")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
