#!/usr/bin/env python3
"""
Demo script for StoryWriterAgent
Shows example usage and capabilities
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from story_agent import StoryAgent
from config import get_api_key, setup_instructions

def demo_story_generation():
    """Demonstrate story generation capabilities"""
    print("📚 StoryWriterAgent Demo")
    print("=" * 50)
    
    # Check API key
    api_key = get_api_key()
    if not api_key:
        print("❌ OpenAI API key not found!")
        print("Please set your API key and run again.")
        setup_instructions()
        return
    
    try:
        # Initialize agent
        agent = StoryAgent(api_key)
        print("✅ StoryWriterAgent initialized successfully!")
        
        # Demo examples
        examples = [
            {
                "prompt": "A dragon who wanted to become a chef",
                "genre": "fantasy",
                "tone": "funny",
                "length": "short",
                "language": "english"
            },
            {
                "prompt": "A robot learning to love in a post-apocalyptic world",
                "genre": "sci-fi",
                "tone": "dramatic",
                "length": "medium",
                "language": "english"
            },
            {
                "prompt": "A detective solving a mystery in space",
                "genre": "mystery",
                "tone": "serious",
                "length": "long",
                "language": "english"
            }
        ]
        
        print(f"\n🎭 Generating {len(examples)} example stories...")
        print("-" * 50)
        
        for i, example in enumerate(examples, 1):
            print(f"\n📖 Example {i}: {example['prompt']}")
            print(f"Genre: {example['genre']} | Tone: {example['tone']} | Length: {example['length']}")
            print("-" * 30)
            
            try:
                story = agent.generate_story(**example)
                
                print(f"Title: {story['title']}")
                print(f"Word Count: {story['word_count']}")
                print(f"Content Preview: {story['content'][:200]}...")
                
                # Save story
                saved_path = agent.save_story(story)
                if saved_path:
                    print(f"💾 Saved to: {saved_path}")
                
                print("✅ Story generated successfully!")
                
            except Exception as e:
                print(f"❌ Error generating story: {e}")
            
            print()
        
        # Show statistics
        print("📊 Demo Statistics:")
        print(f"Total stories generated: {len(examples)}")
        print(f"Stories directory: {agent.stories_dir}")
        
        # Show available options
        print("\n🎨 Available Options:")
        print(f"Genres: {', '.join(agent.get_genres().keys())}")
        print(f"Tones: {', '.join(agent.get_tones().keys())}")
        print(f"Lengths: {', '.join(agent.get_lengths().keys())}")
        print(f"Languages: {', '.join(agent.get_languages().keys())}")
        
        print("\n🎉 Demo completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run: python main.py --web (for web interface)")
        print("2. Run: python main.py --terminal (for terminal interface)")
        print("3. Try: python main.py --quick 'your story idea'")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False
    
    return True

def demo_web_interface():
    """Show web interface information"""
    print("\n🌐 Web Interface Demo")
    print("=" * 30)
    print("To start the web interface:")
    print("1. Run: python main.py --web")
    print("2. Open: http://localhost:8036")
    print("3. Enter a story prompt")
    print("4. Select genre, tone, length, and language")
    print("5. Click 'Generate Story'")
    print("6. Save, favorite, or download your story")

def demo_terminal_interface():
    """Show terminal interface information"""
    print("\n💻 Terminal Interface Demo")
    print("=" * 35)
    print("To start the terminal interface:")
    print("1. Run: python main.py --terminal")
    print("2. Use these commands:")
    print("   - generate <prompt>  # Generate a story")
    print("   - list              # List all stories")
    print("   - search <query>    # Search stories")
    print("   - favorites         # Show favorites")
    print("   - help              # Show help")
    print("   - quit              # Exit")

def main():
    """Main demo function"""
    print("🚀 StoryWriterAgent - Day 36 Demo")
    print("=" * 50)
    
    # Check if we should run the full demo
    if len(sys.argv) > 1 and sys.argv[1] == "--full":
        success = demo_story_generation()
        if not success:
            sys.exit(1)
    else:
        print("📚 StoryWriterAgent is ready!")
        print("\nTo run the full demo with story generation:")
        print("python demo.py --full")
        print("\n(Note: Requires OpenAI API key)")
    
    demo_web_interface()
    demo_terminal_interface()
    
    print("\n🎯 Quick Start:")
    print("python main.py --quick 'A magical library where books come alive'")
    print("python main.py --web")
    print("python main.py --terminal")

if __name__ == "__main__":
    main()
