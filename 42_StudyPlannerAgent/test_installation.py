#!/usr/bin/env python3
"""
StudyPlannerAgent - Installation Test
Test script to verify that all components are working correctly
"""

import sys
import os
from pathlib import Path

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("\n📦 Testing module imports...")
    
    required_modules = [
        ("openai", "OpenAI API client"),
        ("fastapi", "FastAPI web framework"),
        ("uvicorn", "ASGI server"),
        ("jinja2", "Template engine"),
        ("pydantic", "Data validation"),
        ("pathlib", "Path utilities"),
        ("json", "JSON handling"),
        ("datetime", "Date/time utilities")
    ]
    
    all_imports_ok = True
    
    for module_name, description in required_modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - {description}")
        except ImportError as e:
            print(f"❌ {module_name} - {description} (Error: {e})")
            all_imports_ok = False
    
    return all_imports_ok

def test_project_structure():
    """Test if project structure is correct"""
    print("\n📁 Testing project structure...")
    
    required_files = [
        "main.py",
        "config.py",
        "web_app.py",
        "requirements.txt",
        "README.md",
        "cli/studyplanner.py",
        "utils/plan_generator.py",
        "templates/index.html",
        "static/js/app.js"
    ]
    
    all_files_ok = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            all_files_ok = False
    
    return all_files_ok

def test_api_key():
    """Test if OpenAI API key is configured"""
    print("\n🔑 Testing API key configuration...")
    
    # Try to get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        if api_key.startswith("sk-") and len(api_key) > 20:
            print("✅ OpenAI API key found and appears valid")
            return True
        else:
            print("⚠️  OpenAI API key found but format seems incorrect")
            return False
    else:
        print("❌ OpenAI API key not found")
        print("💡 Set your API key using:")
        print("   Windows: set OPENAI_API_KEY=your_api_key_here")
        print("   Linux/Mac: export OPENAI_API_KEY=your_api_key_here")
        print("   Or create a .env file with: OPENAI_API_KEY=your_api_key_here")
        return False

def test_directories():
    """Test if required directories exist and are writable"""
    print("\n📂 Testing directory permissions...")
    
    directories = [
        "output",
        "output/study_plans"
    ]
    
    all_dirs_ok = True
    
    for dir_path in directories:
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            # Test write permission
            test_file = Path(dir_path) / "test_write.tmp"
            test_file.write_text("test")
            test_file.unlink()
            print(f"✅ {dir_path} - Writable")
        except Exception as e:
            print(f"❌ {dir_path} - Error: {e}")
            all_dirs_ok = False
    
    return all_dirs_ok

def test_web_server():
    """Test if web server can start (basic test)"""
    print("\n🌐 Testing web server components...")
    
    try:
        # Test FastAPI import and basic app creation
        from fastapi import FastAPI
        from web_app import create_app
        from utils.plan_generator import StudyPlanGenerator
        
        # Create a test app (without actually starting server)
        app = FastAPI(title="Test App")
        print("✅ FastAPI app creation - OK")
        
        # Test if we can import the plan generator
        print("✅ StudyPlanGenerator import - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Web server test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 StudyPlannerAgent - Installation Test")
    print("=" * 60)
    
    tests = [
        ("Python Version", test_python_version),
        ("Module Imports", test_imports),
        ("Project Structure", test_project_structure),
        ("API Key", test_api_key),
        ("Directory Permissions", test_directories),
        ("Web Server", test_web_server)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! StudyPlannerAgent is ready to use.")
        print("\n🚀 Next steps:")
        print("1. Set your OpenAI API key if not already set")
        print("2. Run: python main.py --web")
        print("3. Open your browser to: http://127.0.0.1:8042")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        print("\n🔧 Common solutions:")
        print("- Run: pip install -r requirements.txt")
        print("- Set your OpenAI API key")
        print("- Check file permissions")
    
    print("\n" + "=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
