#!/usr/bin/env python3
"""
Setup script for SocialPostCreatorAgent
Helps users configure their environment properly
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    env_content = """# OpenAI API Key (REQUIRED - Get from https://platform.openai.com/account/api-keys)
OPENAI_API_KEY=your_openai_api_key_here

# OpenAI Model (optional, defaults to gpt-4o-mini)
OPENAI_MODEL=gpt-4o-mini

# NewsAPI for topic research (optional)
NEWSAPI_KEY=your_newsapi_key_here

# Timezone (optional, defaults to UTC)
TW_TZ=UTC

# Chrome Profile for web automation (optional, defaults to your main profile)
CHROME_PROFILE_PATH=%LOCALAPPDATA%\\Google\\Chrome\\User Data
CHROME_PROFILE_NAME=Default

# Output directory for saved posts (optional, defaults to "posts")
# POSTS_DIR=posts
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")
        print("⚠️  IMPORTANT: Edit .env file and add your OpenAI API key!")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_env_config():
    """Check if environment is properly configured"""
    print("\n🔧 Checking environment configuration...")
    
    # Check if .env exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    # Check OpenAI API key
    from config import Config
    if not Config.OPENAI_API_KEY or Config.OPENAI_API_KEY == "your_openai_api_key_here":
        print("❌ OpenAI API key not set in .env file")
        print("   Please edit .env and set OPENAI_API_KEY=your_actual_api_key")
        return False
    
    print("✅ OpenAI API key is configured")
    
    # Check NewsAPI key (optional)
    if Config.NEWSAPI_KEY and Config.NEWSAPI_KEY != "your_newsapi_key_here":
        print("✅ NewsAPI key is configured")
    else:
        print("⚠️  NewsAPI key not configured (optional)")
    
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
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

def test_basic_functionality():
    """Test basic functionality without API calls"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test imports
        from config import Config
        from ai_service import generate_social_post
        from search_service import fetch_latest_insights
        from poster import save_post_to_file
        
        print("✅ All modules imported successfully")
        
        # Test configuration
        platforms = list(Config.PLATFORM_LIMITS.keys())
        print(f"✅ Supported platforms: {', '.join(platforms)}")
        
        # Test directory creation
        posts_dir = Path(Config.POSTS_DIR)
        posts_dir.mkdir(exist_ok=True)
        print(f"✅ Posts directory ready: {posts_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 SocialPostCreatorAgent - Setup")
    print("=" * 50)
    
    # Step 1: Create .env file
    if not create_env_file():
        print("❌ Setup failed at step 1")
        return 1
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at step 2")
        return 1
    
    # Step 3: Test basic functionality
    if not test_basic_functionality():
        print("❌ Setup failed at step 3")
        return 1
    
    # Step 4: Check environment configuration
    if not check_env_config():
        print("\n⚠️  Environment not fully configured")
        print("   Please complete the setup manually:")
        print("   1. Edit .env file")
        print("   2. Add your OpenAI API key")
        print("   3. Run: python test_installation.py")
        return 1
    
    print("\n🎉 Setup completed successfully!")
    print("\n🚀 Next steps:")
    print("1. Test installation: python test_installation.py")
    print("2. Try CLI: python -m 22_SocialPostCreatorAgent.cli")
    print("3. Try Web UI: python -m 22_SocialPostCreatorAgent.web_app")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
