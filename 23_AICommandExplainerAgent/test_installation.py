#!/usr/bin/env python3
"""
Test script for AICommandExplainerAgent
Verifies installation and basic functionality
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported."""
    print("🔍 Testing package imports...")
    
    try:
        import openai
        print("✅ openai package imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import openai: {e}")
        return False
    
    try:
        import rich
        print("✅ rich package imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import rich: {e}")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv package imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import dotenv: {e}")
        return False
    
    return True

def test_config():
    """Test if configuration can be loaded."""
    print("\n🔍 Testing configuration...")
    
    try:
        from config import OPENAI_API_KEY, OPENAI_MODEL, TEMPERATURE, MAX_TOKENS
        print("✅ Configuration loaded successfully")
        print(f"   Model: {OPENAI_MODEL}")
        print(f"   Temperature: {TEMPERATURE}")
        print(f"   Max Tokens: {MAX_TOKENS}")
        
        if OPENAI_API_KEY:
            print("✅ OpenAI API key found")
        else:
            print("⚠️  OpenAI API key not set (this is expected for testing)")
        
        return True
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        return False

def test_command_explainer():
    """Test if CommandExplainer class can be instantiated."""
    print("\n🔍 Testing CommandExplainer class...")
    
    try:
        from command_explainer import CommandExplainer, detect_os
        
        # Test OS detection
        os_profile = detect_os()
        print(f"✅ OS detection working: {os_profile['name']} using {os_profile['shell']}")
        
        # Test class instantiation (without API key for testing)
        try:
            explainer = CommandExplainer()
            print("✅ CommandExplainer instantiated successfully")
        except ValueError as e:
            if "Missing OpenAI API key" in str(e):
                print("✅ CommandExplainer correctly requires API key")
            else:
                print(f"❌ Unexpected error: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Failed to test CommandExplainer: {e}")
        return False

def test_utility_functions():
    """Test utility functions."""
    print("\n🔍 Testing utility functions...")
    
    try:
        from command_explainer import detect_os
        
        os_profile = detect_os()
        required_keys = ['id', 'name', 'shell']
        
        for key in required_keys:
            if key not in os_profile:
                print(f"❌ Missing key in OS profile: {key}")
                return False
        
        print("✅ OS detection utility working correctly")
        return True
    except Exception as e:
        print(f"❌ Failed to test utility functions: {e}")
        return False

def test_file_structure():
    """Test if all required files exist."""
    print("\n🔍 Testing file structure...")
    
    required_files = [
        'main.py',
        'command_explainer.py',
        'config.py',
        'requirements.txt',
        'README.md',
        'env.example'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_environment_setup():
    """Test environment setup."""
    print("\n🔍 Testing environment setup...")
    
    # Check if .env file exists
    if Path('.env').exists():
        print("✅ .env file found")
        
        # Try to load it
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                print("✅ OpenAI API key loaded from .env")
            else:
                print("⚠️  .env file exists but no API key found")
        except Exception as e:
            print(f"❌ Error loading .env: {e}")
            return False
    else:
        print("⚠️  .env file not found (create one with your API key)")
    
    return True

def run_demo():
    """Run the demo if available."""
    print("\n🔍 Testing demo functionality...")
    
    try:
        from demo import main as demo_main
        print("✅ Demo module imported successfully")
        
        # Note: We won't actually run the demo here as it's interactive
        print("✅ Demo functionality available (run with: python demo.py)")
        return True
    except Exception as e:
        print(f"❌ Failed to test demo: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 AICommandExplainerAgent Installation Test")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Configuration", test_config),
        ("CommandExplainer Class", test_command_explainer),
        ("Utility Functions", test_utility_functions),
        ("File Structure", test_file_structure),
        ("Environment Setup", test_environment_setup),
        ("Demo Functionality", run_demo)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Installation successful!")
        print("\n🚀 Next steps:")
        print("1. Set your OpenAI API key in .env file")
        print("2. Run: python main.py")
        print("3. Or try the demo: python demo.py")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
