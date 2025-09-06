#!/usr/bin/env python3
"""
Test installation for StoryWriterAgent
"""

import sys
import os
from pathlib import Path

def test_python_version():
    """Test Python version"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported. Please use Python 3.8+")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is supported")
    return True

def test_imports():
    """Test required imports"""
    print("\n📦 Testing required imports...")
    
    required_modules = [
        ('openai', 'OpenAI API client'),
        ('fastapi', 'FastAPI web framework'),
        ('uvicorn', 'ASGI server'),
        ('jinja2', 'Template engine'),
        ('pydantic', 'Data validation'),
        ('colorama', 'Terminal colors'),
        ('dotenv', 'Environment variables')
    ]
    
    failed_imports = []
    
    for module, description in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError as e:
            print(f"❌ {module} - {description} (Error: {e})")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    return True

def test_file_structure():
    """Test file structure"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'main.py',
        'config.py',
        'story_agent.py',
        'web_app.py',
        'requirements.txt',
        'templates/index.html',
        'templates/stories.html',
        'static/css/style.css',
        'static/js/app.js',
        'static/js/stories.js'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def test_config():
    """Test configuration"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config import StoryConfig, get_api_key
        
        # Test configuration classes
        config = StoryConfig()
        
        # Test genres
        genres = config.GENRES
        if not genres or len(genres) < 3:
            print("❌ Invalid genres configuration")
            return False
        print(f"✅ Genres configured: {len(genres)} genres")
        
        # Test tones
        tones = config.TONES
        if not tones or len(tones) < 3:
            print("❌ Invalid tones configuration")
            return False
        print(f"✅ Tones configured: {len(tones)} tones")
        
        # Test lengths
        lengths = config.LENGTHS
        if not lengths or len(lengths) < 3:
            print("❌ Invalid lengths configuration")
            return False
        print(f"✅ Lengths configured: {len(lengths)} lengths")
        
        # Test languages
        languages = config.LANGUAGES
        if not languages or len(languages) < 3:
            print("❌ Invalid languages configuration")
            return False
        print(f"✅ Languages configured: {len(languages)} languages")
        
        # Test API key
        api_key = get_api_key()
        if api_key:
            print("✅ OpenAI API key found")
        else:
            print("⚠️  OpenAI API key not found (set OPENAI_API_KEY environment variable)")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_story_agent():
    """Test story agent initialization"""
    print("\n🤖 Testing story agent...")
    
    try:
        from story_agent import StoryAgent
        from config import get_api_key
        
        api_key = get_api_key()
        if not api_key:
            print("⚠️  Skipping story agent test (no API key)")
            return True
        
        # Test agent initialization
        agent = StoryAgent(api_key)
        print("✅ Story agent initialized successfully")
        
        # Test configuration methods
        genres = agent.get_genres()
        tones = agent.get_tones()
        lengths = agent.get_lengths()
        languages = agent.get_languages()
        
        if not all([genres, tones, lengths, languages]):
            print("❌ Failed to get configuration data")
            return False
        
        print("✅ Configuration methods working")
        
        return True
        
    except Exception as e:
        print(f"❌ Story agent test failed: {e}")
        return False

def test_web_app():
    """Test web app initialization"""
    print("\n🌐 Testing web app...")
    
    try:
        from web_app import create_app
        from story_agent import StoryAgent
        from config import get_api_key
        
        api_key = get_api_key()
        if not api_key:
            print("⚠️  Skipping web app test (no API key)")
            return True
        
        # Test app creation
        agent = StoryAgent(api_key)
        app = create_app(agent)
        print("✅ Web app created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Web app test failed: {e}")
        return False

def test_directories():
    """Test directory creation"""
    print("\n📂 Testing directory creation...")
    
    try:
        from story_agent import StoryAgent
        from config import get_api_key
        
        api_key = get_api_key()
        if not api_key:
            print("⚠️  Skipping directory test (no API key)")
            return True
        
        agent = StoryAgent(api_key)
        
        # Check if stories directory exists
        stories_dir = Path("stories")
        if stories_dir.exists():
            print("✅ Stories directory exists")
        else:
            print("✅ Stories directory will be created on first use")
        
        return True
        
    except Exception as e:
        print(f"❌ Directory test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 StoryWriterAgent Installation Test")
    print("=" * 50)
    
    tests = [
        test_python_version,
        test_imports,
        test_file_structure,
        test_config,
        test_story_agent,
        test_web_app,
        test_directories
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! StoryWriterAgent is ready to use.")
        print("\n📋 Next steps:")
        print("1. Set your OpenAI API key in .env file")
        print("2. Run: python main.py --web")
        print("3. Open: http://localhost:8036")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Common solutions:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set OpenAI API key: set OPENAI_API_KEY=your_key_here")
        print("3. Check file permissions and paths")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
