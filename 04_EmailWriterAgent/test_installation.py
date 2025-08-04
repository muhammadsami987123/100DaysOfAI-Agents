#!/usr/bin/env python3
"""
Test script for EmailWriterAgent installation
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import openai
        print("✅ OpenAI module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import OpenAI: {e}")
        return False
    
    try:
        import fastapi
        print("✅ FastAPI module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import FastAPI: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Uvicorn: {e}")
        return False
    
    try:
        import jinja2
        print("✅ Jinja2 module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Jinja2: {e}")
        return False
    
    try:
        import colorama
        print("✅ Colorama module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Colorama: {e}")
        return False
    
    try:
        import pydantic
        print("✅ Pydantic module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Pydantic: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\n🔍 Testing configuration...")
    
    try:
        from config import get_api_key, EmailConfig
        print("✅ Configuration module imported successfully")
        
        # Test config class
        config = EmailConfig()
        print(f"✅ EmailConfig loaded with {len(config.TEMPLATES)} templates")
        
        # Test API key function
        api_key = get_api_key()
        if api_key:
            print("✅ API key found")
        else:
            print("⚠️  No API key found (this is normal if not set)")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_email_agent():
    """Test EmailAgent class"""
    print("\n🔍 Testing EmailAgent...")
    
    try:
        from email_agent import EmailAgent
        print("✅ EmailAgent class imported successfully")
        
        # Test with dummy API key
        agent = EmailAgent("dummy_key")
        print("✅ EmailAgent initialized successfully")
        
        # Test templates
        templates = agent.get_templates()
        print(f"✅ Found {len(templates)} email templates")
        
        return True
    except Exception as e:
        print(f"❌ EmailAgent test failed: {e}")
        return False

def test_web_app():
    """Test web application"""
    print("\n🔍 Testing web application...")
    
    try:
        from web_app import create_app
        print("✅ Web app module imported successfully")
        
        # Test app creation with dummy agent
        from email_agent import EmailAgent
        dummy_agent = EmailAgent("dummy_key")
        app = create_app(dummy_agent)
        print("✅ Web app created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Web app test failed: {e}")
        return False

def test_files():
    """Test if all required files exist"""
    print("\n🔍 Testing file structure...")
    
    required_files = [
        "main.py",
        "email_agent.py",
        "web_app.py",
        "config.py",
        "requirements.txt",
        "README.md",
        "templates/index.html",
        "static/css/style.css",
        "static/js/app.js"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} files")
        return False
    else:
        print("\n✅ All required files present")
        return True

def main():
    """Run all tests"""
    print("🤖 EmailWriterAgent - Installation Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_files),
        ("Module Imports", test_imports),
        ("Configuration", test_config),
        ("Email Agent", test_email_agent),
        ("Web Application", test_web_app)
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
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! EmailWriterAgent is ready to use.")
        print("\nNext steps:")
        print("1. Set your OpenAI API key")
        print("2. Run: python main.py --web")
        print("3. Open http://127.0.0.1:8004 in your browser")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Check that all files are present")
        print("3. Verify Python version (3.8+)")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 