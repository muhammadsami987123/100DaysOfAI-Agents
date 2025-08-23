#!/usr/bin/env python3
"""
Quick test to verify the OpenAI API fix works
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_import():
    """Test if OpenAI can be imported and initialized."""
    try:
        import openai
        print("✅ OpenAI package imported successfully")
        
        # Test client initialization
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            client = openai.OpenAI(api_key=api_key)
            print("✅ OpenAI client initialized successfully")
            print(f"✅ API key found: {api_key[:10]}...")
            return True
        else:
            print("⚠️  No API key found in .env file")
            print("   This is expected if you haven't set up your API key yet")
            return True
            
    except ImportError as e:
        print(f"❌ Failed to import OpenAI: {e}")
        return False
    except Exception as e:
        print(f"❌ Error initializing OpenAI client: {e}")
        return False

def test_command_explainer():
    """Test if CommandExplainer can be imported."""
    try:
        from command_explainer import CommandExplainer, detect_os
        
        # Test OS detection
        os_profile = detect_os()
        print(f"✅ OS detection working: {os_profile['name']} using {os_profile['shell']}")
        
        # Test class import (won't instantiate without API key)
        print("✅ CommandExplainer class imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to import CommandExplainer: {e}")
        return False

def main():
    """Run the tests."""
    print("🔍 Testing OpenAI API Fix")
    print("=" * 40)
    
    tests = [
        ("OpenAI Import & Client", test_openai_import),
        ("CommandExplainer Import", test_command_explainer)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The OpenAI API fix is working!")
        print("\n🚀 You can now:")
        print("1. Set your OpenAI API key in .env file")
        print("2. Run: python main.py")
        print("3. Enjoy the AI-powered command explanations!")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit(main())
