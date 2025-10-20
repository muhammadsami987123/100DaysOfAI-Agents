#!/usr/bin/env python3
"""
Test script for GPTConfigGenerator installation and functionality
"""

import sys
import os
import importlib.util

def test_python_version():
    """Test if Python version is compatible"""
    print("Testing Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported. Please use Python 3.8+")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True

def test_imports():
    """Test if all required modules can be imported"""
    print("\nTesting imports...")
    
    required_modules = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'yaml',
        'toml',
        'dotenv'
    ]
    
    optional_modules = [
        'openai',
        'google.generativeai'
    ]
    
    all_good = True
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            all_good = False
    
    print("\nOptional modules (for AI functionality):")
    for module in optional_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"⚠️  {module}: {e} (AI features will be limited)")
    
    return all_good

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'main.py',
        'agent.py',
        'config.py',
        'utils/__init__.py',
        'utils/llm_service.py',
        'templates/index.html',
        'requirements.txt',
        'env.example',
        'README.md'
    ]
    
    all_good = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} not found")
            all_good = False
    
    return all_good

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from config import Config
        
        # Test basic config loading
        print(f"✅ Config loaded successfully")
        print(f"   LLM Model: {Config.LLM_MODEL}")
        print(f"   Supported Formats: {', '.join(Config.SUPPORTED_FORMATS)}")
        print(f"   Config Types: {len(Config.CONFIG_TYPES)} types available")
        
        # Test validation
        if Config.validate():
            print("✅ Configuration validation passed")
        else:
            print("⚠️  Configuration validation failed (API keys not set)")
        
        return True
        
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_agent():
    """Test agent initialization"""
    print("\nTesting agent...")
    
    try:
        from agent import GPTConfigGenerator
        
        agent = GPTConfigGenerator()
        print("✅ Agent initialized successfully")
        
        # Test basic functionality
        formats = agent.get_supported_formats()
        types = agent.get_config_types()
        
        print(f"   Supported formats: {', '.join(formats)}")
        print(f"   Configuration types: {len(types)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent error: {e}")
        return False

def test_web_app():
    """Test web application"""
    print("\nTesting web application...")
    
    try:
        from main import app
        print("✅ FastAPI app initialized successfully")
        
        # Test if templates exist
        if os.path.exists('templates/index.html'):
            print("✅ HTML template found")
        else:
            print("❌ HTML template not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Web app error: {e}")
        return False

def test_cli():
    """Test CLI interface"""
    print("\nTesting CLI interface...")
    
    try:
        from cli import main
        print("✅ CLI interface loaded successfully")
        
        if os.path.exists('cli.py'):
            print("✅ CLI script found")
        else:
            print("❌ CLI script not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ CLI error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 GPTConfigGenerator Installation Test")
    print("=" * 50)
    
    tests = [
        test_python_version,
        test_imports,
        test_file_structure,
        test_config,
        test_agent,
        test_web_app,
        test_cli
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All tests passed! ({passed}/{total})")
        print("\n✅ GPTConfigGenerator is ready to use!")
        print("\nTo start the application:")
        print("   python main.py")
        print("   Then open http://127.0.0.1:8000 in your browser")
        print("\nTo use CLI:")
        print("   python cli.py 'Create a JSON config for Express app'")
        return 0
    else:
        print(f"⚠️  {passed}/{total} tests passed")
        print("\n❌ Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("   1. Run: pip install -r requirements.txt")
        print("   2. Copy env.example to .env and add your API keys")
        print("   3. Check that all files are in the correct locations")
        return 1

if __name__ == "__main__":
    sys.exit(main())
