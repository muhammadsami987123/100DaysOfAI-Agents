#!/usr/bin/env python3
"""
🔧 TodoAgent Setup Script

This script helps you set up your OpenAI API key and get started with TodoAgent.
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create a .env file in the home directory."""
    home_dir = Path.home()
    env_file = home_dir / ".env"
    
    print(f"🔧 Setting up TodoAgent...")
    print(f"📁 Looking for .env file in: {home_dir}")
    
    if env_file.exists():
        print(f"✅ .env file already exists at: {env_file}")
        return True
    
    print(f"📝 Creating .env file at: {env_file}")
    
    # Get API key from user
    print("\n🔑 Please enter your OpenAI API key:")
    print("   (Get it from: https://platform.openai.com/api-keys)")
    api_key = input("   API Key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return False
    
    # Write to .env file
    try:
        with open(env_file, 'w') as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        print(f"✅ .env file created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
            return True
        else:
            print(f"❌ Error installing dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def test_setup():
    """Test if the setup is working."""
    print("\n🧪 Testing setup...")
    try:
        from config import get_api_key
        api_key = get_api_key()
        if api_key:
            print("✅ API key found and loaded successfully!")
            return True
        else:
            print("❌ API key not found. Please check your .env file.")
            return False
    except Exception as e:
        print(f"❌ Error testing setup: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 TodoAgent Setup")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies. Please run: pip install -r requirements.txt")
        return
    
    # Create .env file
    if not create_env_file():
        print("❌ Failed to create .env file.")
        return
    
    # Test setup
    if not test_setup():
        print("❌ Setup test failed.")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("=" * 50)
    print("🚀 You can now run TodoAgent:")
    print("   python main.py")
    print()
    print("📖 For more information, see README.md")
    print("🤖 Happy todo managing!")

if __name__ == "__main__":
    main() 