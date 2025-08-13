#!/usr/bin/env python3
"""
CodeReviewerBot Installation Test
Day 13 of #100DaysOfAI-Agents

This script tests the installation and basic functionality of CodeReviewerBot.
"""

import os
import sys
import importlib
import subprocess
from pathlib import Path


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)


def print_section(title: str):
    """Print a formatted section."""
    print(f"\n--- {title} ---")


def check_python_version():
    """Check Python version compatibility."""
    print_section("Python Version Check")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python version is compatible (3.8+)")
        return True
    else:
        print("❌ Python version must be 3.8 or higher")
        return False


def check_dependencies():
    """Check if all required dependencies are installed."""
    print_section("Dependencies Check")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'python-multipart',
        'jinja2',
        'python-dotenv',
        'openai',
        'requests',
        'aiofiles'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies are installed")
        return True


def check_configuration():
    """Check configuration files and environment."""
    print_section("Configuration Check")
    
    # Check if .env file exists
    env_file = Path('.env')
    if env_file.exists():
        print("✅ .env file found")
        
        # Check for OpenAI API key
        with open(env_file, 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY' in content:
                print("✅ OpenAI API key found in .env")
            else:
                print("⚠️  OpenAI API key not found in .env")
    else:
        print("⚠️  .env file not found")
        print("   Create .env file with your OpenAI API key")
    
    # Check if config.py can be imported
    try:
        from config import SUPPORTED_LANGUAGES, UI_LANGUAGES
        print(f"✅ Configuration loaded successfully")
        print(f"   Supported languages: {len(SUPPORTED_LANGUAGES)}")
        print(f"   UI languages: {len(UI_LANGUAGES)}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def check_services():
    """Check if services can be initialized."""
    print_section("Services Check")
    
    try:
        from code_review_service import CodeReviewService
        print("✅ CodeReviewService can be imported")
    except Exception as e:
        print(f"❌ CodeReviewService import error: {e}")
        return False
    
    try:
        from github_service import GitHubService
        print("✅ GitHubService can be imported")
    except Exception as e:
        print(f"❌ GitHubService import error: {e}")
        return False
    
    return True


def check_directories():
    """Check if required directories exist."""
    print_section("Directory Structure Check")
    
    required_dirs = [
        'templates',
        'static',
        'static/js',
        'uploads',
        'outputs'
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ - NOT FOUND")
            try:
                os.makedirs(dir_path, exist_ok=True)
                print(f"   Created {dir_path}/")
            except Exception as e:
                print(f"   Failed to create: {e}")
    
    return True


def check_files():
    """Check if required files exist."""
    print_section("File Structure Check")
    
    required_files = [
        'server.py',
        'code_review_service.py',
        'github_service.py',
        'config.py',
        'requirements.txt',
        'templates/index.html',
        'static/js/app.js',
        'install.bat',
        'start.bat',
        'README.md'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NOT FOUND")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {len(missing_files)}")
        return False
    else:
        print(f"\n✅ All required files present")
        return True


def test_server_startup():
    """Test if the server can start without errors."""
    print_section("Server Startup Test")
    
    try:
        # Import the app
        from server import app
        print("✅ FastAPI app imported successfully")
        
        # Check if app has required endpoints
        routes = [route.path for route in app.routes]
        required_routes = ['/', '/api/review', '/api/validate-github', '/api/languages', '/api/health']
        
        for route in required_routes:
            if route in routes:
                print(f"✅ Route {route} found")
            else:
                print(f"❌ Route {route} missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Server startup test failed: {e}")
        return False


def test_code_review_functionality():
    """Test basic code review functionality."""
    print_section("Code Review Functionality Test")
    
    try:
        from code_review_service import CodeReviewService
        from config import get_language_from_content
        
        # Test language detection
        python_code = "def hello(): print('Hello, World!')"
        detected_lang = get_language_from_content(python_code)
        print(f"✅ Language detection: {detected_lang}")
        
        # Test code summary generation
        service = CodeReviewService()
        summary = service.generate_code_summary(python_code, 'python')
        print(f"✅ Code summary generated: {summary['total_lines']} lines")
        
        return True
        
    except Exception as e:
        print(f"❌ Code review functionality test failed: {e}")
        return False


def test_github_service():
    """Test GitHub service functionality."""
    print_section("GitHub Service Test")
    
    try:
        from github_service import GitHubService
        
        service = GitHubService()
        
        # Test URL parsing
        test_url = "https://github.com/user/repo/blob/main/file.py"
        info = service.extract_github_info(test_url)
        
        if info:
            print(f"✅ GitHub URL parsing: {info['type']}")
        else:
            print("❌ GitHub URL parsing failed")
        
        return True
        
    except Exception as e:
        print(f"❌ GitHub service test failed: {e}")
        return False


def run_installation_test():
    """Run the complete installation test."""
    print_header("CodeReviewerBot Installation Test")
    print("Testing installation and basic functionality...")
    
    tests = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Configuration", check_configuration),
        ("Services", check_services),
        ("Directories", check_directories),
        ("Files", check_files),
        ("Server Startup", test_server_startup),
        ("Code Review Functionality", test_code_review_functionality),
        ("GitHub Service", test_github_service),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! CodeReviewerBot is ready to use.")
        print("\nNext steps:")
        print("1. Make sure you have a valid OpenAI API key in your .env file")
        print("2. Run: python server.py")
        print("3. Open: http://localhost:8013")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Run: pip install -r requirements.txt")
        print("- Create .env file with your OpenAI API key")
        print("- Check that all files are present")
    
    return passed == total


if __name__ == "__main__":
    success = run_installation_test()
    sys.exit(0 if success else 1)
