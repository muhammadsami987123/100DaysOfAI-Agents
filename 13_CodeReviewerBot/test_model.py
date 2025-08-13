#!/usr/bin/env python3
"""
Test OpenAI Model Configuration
Day 13 of #100DaysOfAI-Agents

This script tests the OpenAI model configuration and API connectivity.
"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI


def test_openai_connection():
    """Test OpenAI API connection and model availability."""
    print("Testing OpenAI API connection...")
    
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    model = os.getenv('OPENAI_MODEL', 'gpt-4')
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False
    
    print(f"✅ API key found (starts with: {api_key[:10]}...)")
    print(f"🤖 Model configured: {model}")
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Test a simple API call
        print("🔍 Testing API connection...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Hello, this is a test message. Please respond with 'Test successful'."}
            ],
            max_tokens=50
        )
        
        content = response.choices[0].message.content
        print(f"✅ API test successful: {content}")
        
        # Test response_format support
        print("🔍 Testing response_format support...")
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": "Respond with a simple JSON object: {\"test\": \"value\"}"}
                ],
                max_tokens=50,
                response_format={"type": "json_object"}
            )
            print("✅ response_format supported")
            return True
        except Exception as e:
            print(f"⚠️  response_format not supported: {e}")
            print("   The application will use fallback parsing")
            return True
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False


def main():
    """Run the model test."""
    print("=" * 60)
    print(" OpenAI Model Configuration Test")
    print("=" * 60)
    
    success = test_openai_connection()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All tests passed! The model is ready to use.")
        print("\nNext steps:")
        print("1. Run: python server.py")
        print("2. Open: http://localhost:8013")
    else:
        print("❌ Tests failed. Please check your configuration.")
        print("\nCommon issues:")
        print("- Invalid API key")
        print("- Insufficient API credits")
        print("- Network connectivity issues")
    
    print("=" * 60)
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
