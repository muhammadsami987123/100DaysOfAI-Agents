#!/usr/bin/env python3
"""
Configuration file for TodoAgent

This file helps manage API keys and configuration settings.
You can either:
1. Set your OpenAI API key in this file directly
2. Use environment variables
3. Use a .env file in your home directory
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file in home directory
home_dir = os.path.expanduser("~")
env_file = os.path.join(home_dir, ".env")
if os.path.exists(env_file):
    load_dotenv(env_file)

# You can set your API key here directly (not recommended for security)
# OPENAI_API_KEY = "your_api_key_here"

# Or use environment variable (recommended)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def get_api_key():
    """Get the OpenAI API key from various sources."""
    # First check if it's set in this file
    if 'OPENAI_API_KEY' in globals() and OPENAI_API_KEY:
        return OPENAI_API_KEY
    
    # Then check environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        return api_key
    
    return None

def setup_instructions():
    """Print setup instructions."""
    print("🔧 TodoAgent Setup Instructions:")
    print("=" * 50)
    print()
    print("To set up your OpenAI API key, choose one of these methods:")
    print()
    print("1. Create a .env file in your home directory:")
    print(f"   Create file: {os.path.expanduser('~')}/.env")
    print("   Add this line: OPENAI_API_KEY=your_actual_api_key_here")
    print()
    print("2. Set environment variable:")
    print("   Windows: set OPENAI_API_KEY=your_actual_api_key_here")
    print("   macOS/Linux: export OPENAI_API_KEY=your_actual_api_key_here")
    print()
    print("3. Pass as command line argument:")
    print("   python main.py your_actual_api_key_here")
    print()
    print("4. Edit this config.py file (not recommended for security)")
    print()
    print("Get your API key from: https://platform.openai.com/api-keys")
    print()
    print("💡 Quick Setup (Windows):")
    print("   set OPENAI_API_KEY=your_api_key_here")
    print("   python main.py")
    print()
    print("💡 Quick Setup (macOS/Linux):")
    print("   export OPENAI_API_KEY=your_api_key_here")
    print("   python main.py")
    print("=" * 50) 