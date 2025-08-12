#!/usr/bin/env python3
"""
Test script to verify JobApplicationAgent installation
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing package imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import openai
        print("✅ OpenAI imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    try:
        import fitz  # PyMuPDF
        print("✅ PyMuPDF imported successfully")
    except ImportError as e:
        print(f"❌ PyMuPDF import failed: {e}")
        return False
    
    try:
        from docx import Document
        print("✅ python-docx imported successfully")
    except ImportError as e:
        print(f"❌ python-docx import failed: {e}")
        return False
    
    try:
        from reportlab.lib.pagesizes import letter
        print("✅ ReportLab imported successfully")
    except ImportError as e:
        print(f"❌ ReportLab import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup imported successfully")
    except ImportError as e:
        print(f"❌ BeautifulSoup import failed: {e}")
        return False
    
    try:
        import lxml
        print("✅ lxml imported successfully")
    except ImportError as e:
        print(f"❌ lxml import failed: {e}")
        return False
    
    return True

def test_local_modules():
    """Test if local modules can be imported"""
    print("\nTesting local module imports...")
    
    try:
        from config import PORT, OPENAI_API_KEY
        print("✅ Config module imported successfully")
    except ImportError as e:
        print(f"❌ Config module import failed: {e}")
        return False
    
    try:
        from document_processor import DocumentProcessor
        print("✅ Document processor imported successfully")
    except ImportError as e:
        print(f"❌ Document processor import failed: {e}")
        return False
    
    try:
        from job_agent import JobApplicationAgent
        print("✅ Job agent imported successfully")
    except ImportError as e:
        print(f"❌ Job agent import failed: {e}")
        return False
    
    try:
        from document_generator import DocumentGenerator
        print("✅ Document generator imported successfully")
    except ImportError as e:
        print(f"❌ Document generator import failed: {e}")
        return False
    
    try:
        from url_extractor import JobURLExtractor
        print("✅ URL extractor imported successfully")
    except ImportError as e:
        print(f"❌ URL extractor import failed: {e}")
        return False
    
    return True

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        "server.py",
        "config.py",
        "job_agent.py",
        "document_processor.py",
        "document_generator.py",
        "url_extractor.py",
        "requirements.txt",
        "README.md",
        "templates/index.html",
        "static/css/style.css",
        "static/js/app.js"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_environment():
    """Test environment configuration"""
    print("\nTesting environment configuration...")
    
    # Check if .env file exists
    if os.path.exists(".env"):
        print("✅ .env file exists")
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key.startswith("sk-"):
            print("✅ OpenAI API key is configured")
        else:
            print("⚠️  OpenAI API key not configured or invalid")
            print("   Please set OPENAI_API_KEY in your .env file")
    else:
        print("⚠️  .env file not found")
        print("   Please create .env file with your OpenAI API key")
    
    return True

def test_server_startup():
    """Test if server can start (without actually starting it)"""
    print("\nTesting server startup...")
    
    try:
        # Import server components
        from server import app
        
        # Check if FastAPI app was created
        if hasattr(app, 'routes'):
            print("✅ FastAPI app created successfully")
            print(f"   Found {len(app.routes)} routes")
        else:
            print("❌ FastAPI app creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Server startup test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("=" * 50)
    print("JobApplicationAgent - Installation Test")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Local Modules", test_local_modules),
        ("File Structure", test_file_structure),
        ("Environment", test_environment),
        ("Server Startup", test_server_startup)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! JobApplicationAgent is ready to use.")
        print("\nNext steps:")
        print("1. Create a .env file with your OpenAI API key")
        print("2. Run: python server.py")
        print("3. Open: http://localhost:8012")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check that all files are present in the correct locations")
        print("3. Verify your .env file configuration")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
