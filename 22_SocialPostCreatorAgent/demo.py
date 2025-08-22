#!/usr/bin/env python3
"""
Demo script for SocialPostCreatorAgent
Showcases the main features without requiring user interaction
"""

import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def demo_config():
    """Demo the configuration system"""
    print("🔧 Configuration Demo")
    print("-" * 40)
    
    try:
        from config import Config
        
        print(f"✅ OpenAI Model: {Config.OPENAI_MODEL}")
        print(f"✅ Supported Platforms: {', '.join(Config.PLATFORM_LIMITS.keys())}")
        print(f"✅ Default Platform: {Config.DEFAULT_PLATFORM}")
        print(f"✅ Posts Directory: {Config.POSTS_DIR}")
        
        # Show platform limits
        print("\n📱 Platform Character Limits:")
        for platform, limit in Config.PLATFORM_LIMITS.items():
            print(f"   {platform}: {limit:,} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration demo failed: {e}")
        return False


def demo_ai_service():
    """Demo the AI service (without making API calls)"""
    print("\n🤖 AI Service Demo")
    print("-" * 40)
    
    try:
        from ai_service import generate_social_post, generate_tweet
        
        print("✅ AI service functions imported successfully")
        print("✅ generate_social_post() - Multi-platform post generation")
        print("✅ generate_tweet() - Twitter-specific generation (legacy)")
        
        # Show available tones
        from cli import get_available_tones
        tones = get_available_tones()
        print(f"✅ Available Tones: {', '.join(tones)}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI service demo failed: {e}")
        return False


def demo_search_service():
    """Demo the search service"""
    print("\n🔍 Search Service Demo")
    print("-" * 40)
    
    try:
        from search_service import fetch_latest_insights
        
        print("✅ Search service imported successfully")
        print("✅ fetch_latest_insights() - Topic research functionality")
        
        # Check if NewsAPI key is available
        from config import Config
        if Config.NEWSAPI_KEY:
            print("✅ NewsAPI key is configured")
        else:
            print("⚠️  NewsAPI key not configured (optional)")
        
        return True
        
    except Exception as e:
        print(f"❌ Search service demo failed: {e}")
        return False


def demo_poster_service():
    """Demo the poster service"""
    print("\n📝 Poster Service Demo")
    print("-" * 40)
    
    try:
        from poster import save_post_to_file, save_tweet_to_file
        
        print("✅ Poster service imported successfully")
        print("✅ save_post_to_file() - Multi-platform post saving")
        print("✅ save_tweet_to_file() - Twitter-specific saving (legacy)")
        
        # Check if posts directory exists
        posts_dir = Path("posts")
        if posts_dir.exists():
            print(f"✅ Posts directory exists: {posts_dir}")
        else:
            print(f"⚠️  Posts directory will be created: {posts_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ Poster service demo failed: {e}")
        return False


def demo_cli():
    """Demo the CLI interface"""
    print("\n💻 CLI Interface Demo")
    print("-" * 40)
    
    try:
        from cli import get_available_platforms, get_available_tones
        
        platforms = get_available_platforms()
        tones = get_available_tones()
        
        print("✅ CLI interface imported successfully")
        print(f"✅ Available Platforms: {len(platforms)}")
        print(f"✅ Available Tones: {len(tones)}")
        
        print("\n📱 Platform Options:")
        for i, platform in enumerate(platforms, 1):
            print(f"   {i}. {platform}")
        
        print("\n🎨 Tone Options:")
        for i, tone in enumerate(tones, 1):
            print(f"   {i}. {tone}")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI demo failed: {e}")
        return False


def demo_web_app():
    """Demo the web application"""
    print("\n🌐 Web Application Demo")
    print("-" * 40)
    
    try:
        from web_app import app
        
        print("✅ Web application imported successfully")
        print("✅ Flask app created successfully")
        print("✅ Routes configured:")
        
        # Show available routes
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{rule.rule} ({', '.join(rule.methods)})")
        
        for route in routes:
            print(f"   {route}")
        
        return True
        
    except Exception as e:
        print(f"❌ Web app demo failed: {e}")
        return False


def demo_usage_examples():
    """Show usage examples"""
    print("\n📚 Usage Examples")
    print("-" * 40)
    
    examples = [
        {
            "title": "CLI - Interactive Mode",
            "command": "python -m 22_SocialPostCreatorAgent.cli",
            "description": "Start interactive CLI with prompts for platform, topic, and tone"
        },
        {
            "title": "CLI - Quick Generation",
            "command": 'python -m 22_SocialPostCreatorAgent.cli --platform "LinkedIn" --topic "AI in Healthcare" --tone "professional"',
            "description": "Generate a LinkedIn post about AI in healthcare with professional tone"
        },
        {
            "title": "CLI - Save and Copy",
            "command": 'python -m 22_SocialPostCreatorAgent.cli --platform "Instagram" --topic "Sustainable Living" --tone "inspirational" --save --copy',
            "description": "Generate Instagram post, save to file, and copy to clipboard"
        },
        {
            "title": "Web UI",
            "command": "python -m 22_SocialPostCreatorAgent.web_app",
            "description": "Start web server and open http://localhost:5000 in browser"
        },
        {
            "title": "Windows Launcher",
            "command": "start.bat",
            "description": "Use interactive launcher for guided setup (Windows only)"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['title']}")
        print(f"   Command: {example['command']}")
        print(f"   Description: {example['description']}")
        print()
    
    return True


def demo_file_structure():
    """Show the file structure"""
    print("\n📁 Project Structure")
    print("-" * 40)
    
    structure = """
22_SocialPostCreatorAgent/
├── 📄 config.py              # Configuration and platform settings
├── 🤖 ai_service.py          # AI content generation service
├── 🔍 search_service.py      # Topic research and insights
├── 📝 poster.py              # Post saving and file management
├── 💻 cli.py                 # Command-line interface
├── 🌐 web_app.py             # Flask web application
├── 📱 templates/             # HTML templates for web UI
│   └── index.html           # Main web interface
├── 🎨 static/js/            # JavaScript for web UI
│   └── app.js               # Frontend functionality
├── 📚 README.md              # Comprehensive documentation
├── 🔧 requirements.txt       # Python dependencies
├── 🧪 test_installation.py  # Installation verification
├── 🚀 start.bat             # Windows launcher
├── 📦 install.bat           # Windows installer
└── 🌍 env.example           # Environment variables template
"""
    
    print(structure)
    return True


def main():
    """Run all demos"""
    print("🚀 SocialPostCreatorAgent - Feature Demo")
    print("=" * 60)
    
    demos = [
        demo_config,
        demo_ai_service,
        demo_search_service,
        demo_poster_service,
        demo_cli,
        demo_web_app,
        demo_usage_examples,
        demo_file_structure
    ]
    
    passed = 0
    total = len(demos)
    
    for demo in demos:
        try:
            if demo():
                passed += 1
        except Exception as e:
            print(f"❌ Demo {demo.__name__} crashed: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Demo Results: {passed}/{total} demos completed successfully")
    
    if passed == total:
        print("\n🎉 All demos completed! SocialPostCreatorAgent is ready to use.")
        print("\n🚀 Next Steps:")
        print("1. Set your OPENAI_API_KEY in .env file")
        print("2. Run: python test_installation.py")
        print("3. Try: python -m 22_SocialPostCreatorAgent.cli")
        print("4. Or: python -m 22_SocialPostCreatorAgent.web_app")
    else:
        print("\n⚠️  Some demos failed. Please check the errors above.")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
