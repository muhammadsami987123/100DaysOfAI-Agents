#!/usr/bin/env python3
"""
CodeReviewerBot Setup Script
Day 13 of #100DaysOfAI-Agents

This script helps users set up the CodeReviewerBot application.
"""

import os
import sys
from pathlib import Path


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)


def print_section(title: str):
    """Print a formatted section."""
    print(f"\n--- {title} ---")


def check_env_file():
    """Check if .env file exists and has required configuration."""
    print_section("Environment Configuration Check")
    
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ .env file not found")
        print("\nTo fix this:")
        print("1. Copy env.example to .env:")
        print("   cp env.example .env")
        print("2. Edit .env and add your OpenAI API key:")
        print("   OPENAI_API_KEY=sk-your-actual-api-key-here")
        return False
    
    print("✅ .env file found")
    
    # Check for OpenAI API key
    with open(env_file, 'r') as f:
        content = f.read()
        
    if 'OPENAI_API_KEY' not in content:
        print("❌ OPENAI_API_KEY not found in .env file")
        return False
    
    if 'sk-your-openai-api-key-here' in content:
        print("❌ Please replace the placeholder API key with your actual OpenAI API key")
        return False
    
    print("✅ OpenAI API key configured")
    return True


def get_openai_api_key():
    """Get OpenAI API key from user input."""
    print_section("OpenAI API Key Setup")
    
    print("To use CodeReviewerBot, you need an OpenAI API key.")
    print("\nTo get an API key:")
    print("1. Go to https://platform.openai.com/api-keys")
    print("2. Sign in or create an account")
    print("3. Click 'Create new secret key'")
    print("4. Copy the key (starts with 'sk-')")
    
    api_key = input("\nEnter your OpenAI API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("Skipping API key setup. You can add it later to the .env file.")
        return None
    
    if not api_key.startswith('sk-'):
        print("❌ Invalid API key format. OpenAI API keys start with 'sk-'")
        return None
    
    return api_key


def create_env_file(api_key: str = None):
    """Create .env file with configuration."""
    print_section("Creating .env File")
    
    env_content = f"""# CodeReviewerBot Environment Configuration

# OpenAI Configuration (REQUIRED)
OPENAI_API_KEY={api_key or 'sk-your-openai-api-key-here'}

# Server Configuration (Optional - defaults shown)
PORT=8013
HOST=0.0.0.0
DEBUG=False

# File Upload Configuration (Optional - defaults shown)
MAX_FILE_SIZE=10485760

# OpenAI Model Configuration (Optional - defaults shown)
OPENAI_MODEL=gpt-4
MAX_TOKENS=4000
TEMPERATURE=0.3
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created")
    
    if not api_key:
        print("⚠️  Remember to replace 'sk-your-openai-api-key-here' with your actual API key")


def install_dependencies():
    """Install required dependencies."""
    print_section("Installing Dependencies")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def run_setup():
    """Run the complete setup process."""
    print_header("CodeReviewerBot Setup")
    print("This script will help you set up CodeReviewerBot for first use.")
    
    # Check if .env exists and is properly configured
    if check_env_file():
        print("\n✅ Configuration looks good!")
        return True
    
    # Offer to help set up the API key
    api_key = get_openai_api_key()
    
    # Create .env file
    create_env_file(api_key)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup incomplete. Please install dependencies manually:")
        print("   pip install -r requirements.txt")
        return False
    
    print_header("Setup Complete!")
    print("CodeReviewerBot is now configured and ready to use.")
    print("\nNext steps:")
    print("1. If you didn't add your API key, edit .env and add it")
    print("2. Run the application:")
    print("   python server.py")
    print("3. Open your browser to: http://localhost:8013")
    
    return True


if __name__ == "__main__":
    success = run_setup()
    sys.exit(0 if success else 1)
