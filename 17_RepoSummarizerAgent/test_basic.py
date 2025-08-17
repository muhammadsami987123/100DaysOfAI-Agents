#!/usr/bin/env python3
"""
Basic functionality test for RepoSummarizerAgent - Day 17 of #100DaysOfAI-Agents

This script tests basic functionality without requiring API keys.
"""

import sys
import os
from pathlib import Path


def test_file_structure():
    """Test if all required files exist."""
    print("📁 Testing file structure...")
    
    required_files = [
        "config.py",
        "github_service.py", 
        "ai_summarizer.py",
        "main.py",
        "requirements.txt",
        "install.bat",
        "start.bat",
        "setup.py",
        "README.md",
        "env.example"
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


def test_config_import():
    """Test if config module can be imported and basic functions work."""
    print("\n🔧 Testing config module...")
    
    try:
        from config import SUPPORTED_LANGUAGES, get_language_config
        
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
        print(f"❌ Config module test failed: {e}")
        return False


def test_github_service_structure():
    """Test if GitHub service module can be imported."""
    print("\n🌐 Testing GitHub service module...")
    
    try:
        from github_service import GitHubService
        
        # Test class instantiation (without API calls)
        service = GitHubService()
        print("✅ GitHub service module imported successfully")
        
        # Test URL parsing method exists
        if hasattr(service, 'parse_github_url'):
            print("✅ URL parsing method available")
        else:
            print("❌ URL parsing method missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ GitHub service test failed: {e}")
        return False


def test_ai_summarizer_structure():
    """Test if AI summarizer module can be imported."""
    print("\n🤖 Testing AI summarizer module...")
    
    try:
        from ai_summarizer import AISummarizer
        
        # Test class structure (will fail without API key, but that's expected)
        try:
            summarizer = AISummarizer()
            print("✅ AI summarizer module imported successfully")
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


def test_main_module():
    """Test if main module can be imported."""
    print("\n🚀 Testing main module...")
    
    try:
        from main import RepoSummarizerAgent
        
        # Test class instantiation
        agent = RepoSummarizerAgent()
        print("✅ Main module imported successfully")
        
        # Test if required methods exist
        required_methods = ['setup_services', 'run', 'analyze_repository']
        for method in required_methods:
            if hasattr(agent, method):
                print(f"✅ {method} method available")
            else:
                print(f"❌ {method} method missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Main module test failed: {e}")
        return False


def test_requirements():
    """Test if requirements.txt is properly formatted."""
    print("\n📦 Testing requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        required_packages = ['openai', 'requests', 'python-dotenv']
        missing_packages = []
        
        for package in required_packages:
            if package in content:
                print(f"✅ {package}")
            else:
                print(f"❌ {package} - NOT FOUND")
                missing_packages.append(package)
        
        if missing_packages:
            print(f"\n❌ Missing packages in requirements.txt: {', '.join(missing_packages)}")
            return False
        
        print("✅ All required packages listed in requirements.txt")
        return True
        
    except Exception as e:
        print(f"❌ Requirements test failed: {e}")
        return False


def main():
    """Run all basic tests."""
    print("🚀 RepoSummarizerAgent - Day 17 Basic Functionality Test")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Requirements", test_requirements),
        ("Config Module", test_config_import),
        ("GitHub Service", test_github_service_structure),
        ("AI Summarizer", test_ai_summarizer_structure),
        ("Main Module", test_main_module)
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
    print("📊 Basic Test Results Summary")
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
        print("\n🎉 All basic tests passed! RepoSummarizerAgent structure is correct.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up your .env file with OpenAI API key")
        print("3. Run full tests: python test_installation.py")
        print("4. Start analyzing: python main.py --url <github-url>")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
