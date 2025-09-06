#!/usr/bin/env python3
"""
📚 StoryWriterAgent - Day 36 of #100DaysOfAI-Agents

A creative AI agent that generates engaging short stories from simple prompts.
Supports multiple genres, tones, and story lengths with both web UI and terminal interfaces.

Features:
- Natural language story generation with GPT
- Multiple genres (Fantasy, Sci-Fi, Mystery, Romance, Horror, Children's)
- Tone selection (Serious, Funny, Inspirational, Dramatic)
- Story length options (Short, Medium, Long)
- Multilingual support (English, Urdu, Arabic, etc.)
- Story management and favorites
- Download stories as TXT or MD files
- Web UI with rich text display
- Terminal interface for quick story generation

Author: Muhammad Sami Asghar Mughal
"""

import argparse
import sys
import uvicorn
from pathlib import Path

from story_agent import StoryAgent
from web_app import create_app
from config import get_api_key, setup_instructions

def main():
    """Main entry point for StoryWriterAgent"""
    parser = argparse.ArgumentParser(
        description="StoryWriterAgent - AI-powered creative story generation tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --web                    # Start web interface
  python main.py --terminal               # Start terminal interface
  python main.py --quick "A dragon who wanted to become a chef"  # Quick story via terminal
  python main.py --quick "Space adventure" --genre sci-fi --tone funny  # Quick story with options
        """
    )
    
    parser.add_argument(
        "--web", 
        action="store_true", 
        help="Start web interface (default)"
    )
    
    parser.add_argument(
        "--terminal", 
        action="store_true", 
        help="Start terminal interface"
    )
    
    parser.add_argument(
        "--quick", 
        type=str, 
        help="Generate a quick story with the given prompt"
    )
    
    parser.add_argument(
        "--genre", 
        type=str, 
        default="fantasy",
        choices=["fantasy", "sci-fi", "mystery", "romance", "horror", "children"],
        help="Genre for quick story generation (default: fantasy)"
    )
    
    parser.add_argument(
        "--tone", 
        type=str, 
        default="serious",
        choices=["serious", "funny", "inspirational", "dramatic"],
        help="Tone for quick story generation (default: serious)"
    )
    
    parser.add_argument(
        "--length", 
        type=str, 
        default="medium",
        choices=["short", "medium", "long"],
        help="Length for quick story generation (default: medium)"
    )
    
    parser.add_argument(
        "--language", 
        type=str, 
        default="english",
        help="Language for story generation (default: english)"
    )
    
    parser.add_argument(
        "--host", 
        default="127.0.0.1", 
        help="Host for web interface (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8036, 
        help="Port for web interface (default: 8036)"
    )
    
    args = parser.parse_args()
    
    # Check API key
    api_key = get_api_key()
    if not api_key:
        print("❌ Error: OpenAI API key not found!")
        print()
        setup_instructions()
        sys.exit(1)
    
    # Initialize story agent
    try:
        story_agent = StoryAgent(api_key)
        print("✅ StoryWriterAgent initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing StoryWriterAgent: {e}")
        sys.exit(1)
    
    # Handle different modes
    if args.quick:
        # Quick story generation via terminal
        print(f"📚 Generating quick story for: {args.quick}")
        print(f"🎭 Genre: {args.genre} | Tone: {args.tone} | Length: {args.length}")
        
        story_data = story_agent.generate_story(
            prompt=args.quick,
            genre=args.genre,
            tone=args.tone,
            length=args.length,
            language=args.language
        )
        
        print("\n" + "="*60)
        print("📚 GENERATED STORY")
        print("="*60)
        print(f"Title: {story_data['title']}")
        print(f"Genre: {story_data['genre']} | Tone: {story_data['tone']}")
        print(f"Length: {story_data['length']} | Language: {story_data['language']}")
        print("-" * 60)
        print(story_data['content'])
        print("="*60)
        
        # Save story
        saved_path = story_agent.save_story(story_data)
        if saved_path:
            print(f"💾 Story saved to: {saved_path}")
        
    elif args.terminal:
        # Terminal interface
        print("📚 StoryWriterAgent - Terminal Mode")
        print("Type 'help' for commands, 'quit' to exit")
        story_agent.run_terminal()
        
    else:
        # Web interface (default)
        print(f"🌐 Starting StoryWriterAgent web interface...")
        print(f"📚 Open your browser to: http://{args.host}:{args.port}")
        print("Press Ctrl+C to stop the server")
        
        app = create_app(story_agent)
        uvicorn.run(
            app, 
            host=args.host, 
            port=args.port,
            log_level="info"
        )

if __name__ == "__main__":
    main()
