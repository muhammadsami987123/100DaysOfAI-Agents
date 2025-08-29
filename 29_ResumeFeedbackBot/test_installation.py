#!/usr/bin/env python3
"""
ResumeFeedbackBot Installation Test
Tests all components to ensure proper installation
"""

import os
import sys
import json
import requests
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import openai
        print("✅ OpenAI imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    try:
        import PyPDF2
        print("✅ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"❌ PyPDF2 import failed: {e}")
        return False
    
    try:
        from docx import Document
        print("✅ python-docx imported successfully")
    except ImportError as e:
        print(f"❌ python-docx import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup imported successfully")
    except ImportError as e:
        print(f"❌ BeautifulSoup import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\n🔍 Testing configuration...")
    
    try:
        from config import Config
        print("✅ Config module imported successfully")
        
        # Test configuration validation
        errors = Config.validate_config()
        if errors:
            print("⚠️ Configuration warnings:")
            for error in errors:
                print(f"   - {error}")
        else:
            print("✅ Configuration validation passed")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_directory_structure():
    """Test if required directories exist"""
    print("\n🔍 Testing directory structure...")
    
    required_dirs = ['uploads', 'outputs', 'logs', 'templates', 'static']
    missing_dirs = []
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory missing")
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"\nCreating missing directories: {missing_dirs}")
        for dir_name in missing_dirs:
            try:
                os.makedirs(dir_name, exist_ok=True)
                print(f"✅ Created {dir_name}/ directory")
            except Exception as e:
                print(f"❌ Failed to create {dir_name}/ directory: {e}")
                return False
    
    return True

def test_file_structure():
    """Test if required files exist"""
    print("\n🔍 Testing file structure...")
    
    required_files = [
        'server.py',
        'resume_analyzer.py',
        'portfolio_analyzer.py',
        'cli.py',
        'config.py',
        'requirements.txt',
        'README.md',
        'templates/index.html'
    ]
    
    missing_files = []
    
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name} exists")
        else:
            print(f"❌ {file_name} missing")
            missing_files.append(file_name)
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    
    return True

def test_openai_connection():
    """Test OpenAI API connection"""
    print("\n🔍 Testing OpenAI connection...")
    
    try:
        from config import Config
        
        if not Config.OPENAI_API_KEY or Config.OPENAI_API_KEY == 'your_openai_api_key_here':
            print("⚠️ OpenAI API key not configured")
            print("   Please add your API key to the .env file")
            return False
        
        import openai
        client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # Test with a simple request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        
        print("✅ OpenAI API connection successful")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API connection failed: {e}")
        return False

def test_analyzers():
    """Test analyzer classes"""
    print("\n🔍 Testing analyzers...")
    
    try:
        from resume_analyzer import ResumeAnalyzer
        from portfolio_analyzer import PortfolioAnalyzer
        
        # Test resume analyzer initialization
        resume_analyzer = ResumeAnalyzer()
        print("✅ ResumeAnalyzer initialized successfully")
        
        # Test portfolio analyzer initialization
        portfolio_analyzer = PortfolioAnalyzer()
        print("✅ PortfolioAnalyzer initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Analyzer test failed: {e}")
        return False

def test_web_server():
    """Test web server startup"""
    print("\n🔍 Testing web server...")
    
    try:
        from server import app
        
        # Test if Flask app can be created
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/api/health')
            if response.status_code == 200:
                print("✅ Web server health check passed")
                return True
            else:
                print(f"❌ Health check failed with status {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Web server test failed: {e}")
        return False

def test_cli():
    """Test CLI interface"""
    print("\n🔍 Testing CLI interface...")
    
    try:
        from cli import ResumeFeedbackBotCLI
        
        cli = ResumeFeedbackBotCLI()
        print("✅ CLI interface initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def create_sample_resume():
    """Create a sample resume for testing"""
    print("\n🔍 Creating sample resume for testing...")
    
    sample_resume_content = """
JOHN DOE
Software Engineer
john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe

SUMMARY
Experienced software engineer with 5+ years developing web applications using Python, JavaScript, and React. Passionate about creating scalable solutions and mentoring junior developers.

EXPERIENCE
Senior Software Engineer | TechCorp | 2020-2023
• Led development of microservices architecture serving 1M+ users
• Mentored 3 junior developers and improved team productivity by 25%
• Implemented CI/CD pipeline reducing deployment time by 60%

Software Engineer | StartupXYZ | 2018-2020
• Developed full-stack web applications using React and Node.js
• Collaborated with design team to implement responsive UI components
• Reduced application load time by 40% through optimization

EDUCATION
Bachelor of Science in Computer Science | University of Technology | 2018

SKILLS
Programming: Python, JavaScript, React, Node.js, SQL
Tools: Git, Docker, AWS, Jenkins
Soft Skills: Leadership, Problem Solving, Team Collaboration
"""
    
    try:
        with open('sample_resume.txt', 'w', encoding='utf-8') as f:
            f.write(sample_resume_content)
        print("✅ Sample resume created: sample_resume.txt")
        return True
    except Exception as e:
        print(f"❌ Failed to create sample resume: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 ResumeFeedbackBot Installation Test")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_config),
        ("Directory Structure Test", test_directory_structure),
        ("File Structure Test", test_file_structure),
        ("Analyzer Test", test_analyzers),
        ("Web Server Test", test_web_server),
        ("CLI Test", test_cli),
        ("Sample Resume Creation", create_sample_resume)
    ]
    
    # Skip OpenAI test if API key not configured
    from config import Config
    if Config.OPENAI_API_KEY and Config.OPENAI_API_KEY != 'your_openai_api_key_here':
        tests.append(("OpenAI Connection Test", test_openai_connection))
    else:
        print("\n⚠️ Skipping OpenAI connection test (API key not configured)")
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All tests passed! ResumeFeedbackBot is ready to use.")
        print("\nNext steps:")
        print("1. Add your OpenAI API key to the .env file")
        print("2. Start the web server: python server.py")
        print("3. Or use the CLI: python cli.py interactive")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Run: pip install -r requirements.txt")
        print("2. Check if all files are present")
        print("3. Verify your OpenAI API key in .env file")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
