"""
Demo: ArticleRewriter Desktop Application
This example shows how to create a desktop app for ArticleRewriter
"""

import sys
import os
from pathlib import Path

# Add the DesktopAgentWrapper to the path
sys.path.append(str(Path(__file__).parent.parent))

from desktop_gui import DesktopAgentWrapper
from agents.article_rewriter_wrapper import ArticleRewriterWrapper

def main():
    """Create and run ArticleRewriter desktop application"""
    
    print("🖥️ Starting ArticleRewriter Desktop Application...")
    print("=" * 50)
    
    try:
        # Create ArticleRewriter wrapper
        article_wrapper = ArticleRewriterWrapper()
        
        # Create desktop wrapper
        desktop_wrapper = DesktopAgentWrapper(
            agent_class=article_wrapper.agent_class,
            agent_name=article_wrapper.agent_name,
            description=article_wrapper.description,
            ui_config=article_wrapper.get_ui_config()
        )
        
        print("✅ ArticleRewriter wrapper created successfully")
        print("🚀 Starting desktop application...")
        print()
        
        # Run the desktop application
        desktop_wrapper.run()
        
    except Exception as e:
        print(f"❌ Error creating ArticleRewriter desktop app: {e}")
        print("\n💡 Make sure you have:")
        print("1. Installed all dependencies: pip install -r requirements.txt")
        print("2. Set your API keys in .env file")
        print("3. ArticleRewriter agent is available")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
