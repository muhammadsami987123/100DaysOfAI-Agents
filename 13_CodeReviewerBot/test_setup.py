#!/usr/bin/env python3
"""
CodeReviewerBot Setup Test
Day 13 of #100DaysOfAI-Agents

This script tests if the CodeReviewerBot is properly configured.
"""

import os
import sys
from pathlib import Path


def test_configuration():
    """Test if the application is properly configured."""
    print("Testing CodeReviewerBot configuration...")
    
    # Check if .env file exists
    if not Path('.env').exists():
        print("❌ .env file not found")
        print("   Run: python setup.py")
        return False
    
    # Check if OpenAI API key is configured
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'sk-your-openai-api-key-here':
            print("❌ OpenAI API key not configured")
            print("   Edit .env file and add your API key")
            return False
        
        print("✅ OpenAI API key configured")
        
    except ImportError:
        print("❌ python-dotenv not installed")
        print("   Run: pip install python-dotenv")
        return False
    
    # Test imports
    try:
        from config import SUPPORTED_LANGUAGES, validate_config
        from code_review_service import CodeReviewService
        from github_service import GitHubService
        print("✅ All modules imported successfully")
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test configuration validation
    errors = validate_config()
    if errors:
        print(f"❌ Configuration errors: {errors}")
        return False
    
    print("✅ Configuration validation passed")
    
    # Test service initialization
    try:
        service = CodeReviewService()
        print("✅ CodeReviewService initialized successfully")
    except Exception as e:
        print(f"❌ Service initialization failed: {e}")
        return False
    
    print("\n🎉 All tests passed! CodeReviewerBot is ready to use.")
    print("\nNext steps:")
    print("1. Run: python server.py")
    print("2. Open: http://localhost:8013")
    
    return True


if __name__ == "__main__":
    success = test_configuration()
    sys.exit(0 if success else 1)
