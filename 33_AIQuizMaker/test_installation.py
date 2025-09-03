#!/usr/bin/env python3
"""
Test script for AI Quiz Maker installation

This script verifies that all dependencies are properly installed
and the core modules can be imported successfully.
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported."""
    try:
        if package_name:
            importlib.import_module(package_name)
        else:
            importlib.import_module(module_name)
        print(f"✅ {module_name}")
        return True
    except ImportError as e:
        print(f"❌ {module_name}: {e}")
        return False
    except Exception as e:
        print(f"❌ {module_name}: Unexpected error - {e}")
        return False

def test_config():
    """Test configuration module."""
    try:
        from config import get_api_key, validate_config, setup_instructions
        print("✅ Configuration module")
        
        # Test API key retrieval
        api_key = get_api_key()
        if api_key:
            print(f"   API Key: {'✅ Set' if api_key.startswith('sk-') else '❌ Invalid format'}")
        else:
            print("   API Key: ❌ Not set")
        
        # Test configuration validation
        issues = validate_config()
        if issues:
            print(f"   Config Issues: {'❌ ' + ', '.join(issues)}")
        else:
            print("   Config: ✅ Valid")
        
        return True
    except Exception as e:
        print(f"❌ Configuration module: {e}")
        return False

def test_quiz_generator():
    """Test quiz generator module."""
    try:
        from quiz_generator import QuizGenerator
        print("✅ Quiz Generator module")
        
        # Test class instantiation (without API key)
        try:
            generator = QuizGenerator(api_key="test_key")
            print("   Class: ✅ Can instantiate")
        except ValueError:
            print("   Class: ✅ Properly validates API key")
        
        return True
    except Exception as e:
        print(f"❌ Quiz Generator module: {e}")
        return False

def test_flask():
    """Test Flask installation."""
    try:
        import flask
        print(f"✅ Flask {flask.__version__}")
        return True
    except Exception as e:
        print(f"❌ Flask: {e}")
        return False

def test_openai():
    """Test OpenAI client."""
    try:
        import openai
        print(f"✅ OpenAI {openai.__version__}")
        return True
    except Exception as e:
        print(f"❌ OpenAI: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 AI Quiz Maker - Installation Test")
    print("=" * 50)
    print()
    
    # Test core dependencies
    print("Testing core dependencies:")
    print("-" * 30)
    
    tests = [
        ("Python version", lambda: f"✅ Python {sys.version.split()[0]}"),
        ("Flask", test_flask),
        ("OpenAI", test_openai),
        ("Configuration", test_config),
        ("Quiz Generator", test_quiz_generator),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Installation is successful.")
        print("\nNext steps:")
        print("1. Set your OpenAI API key:")
        print("   set OPENAI_API_KEY=your_api_key_here")
        print("\n2. Run the web interface:")
        print("   python server.py")
        print("\n3. Or use the CLI:")
        print("   python main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Run install.bat (Windows) or pip install -r requirements.txt")
        print("2. Check Python version (3.8+ required)")
        print("3. Verify all dependencies are installed")
    
    print("\nFor more help, see README.md")

if __name__ == "__main__":
    main()
