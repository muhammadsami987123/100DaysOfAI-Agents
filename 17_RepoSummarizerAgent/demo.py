#!/usr/bin/env python3
"""
Demo script for RepoSummarizerAgent - Day 17 of #100DaysOfAI-Agents

This script demonstrates the agent's capabilities with example repositories.
"""

import sys
import os
from pathlib import Path


def show_demo_banner():
    """Display the demo banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🎯 RepoSummarizerAgent Demo                             ║
║                                                                              ║
║           Showcasing AI-powered GitHub repository analysis                  ║
║                                                                              ║
║                    Part of #100DaysOfAI-Agents Challenge                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
    print(banner)


def show_example_repositories():
    """Show example repositories for demonstration."""
    examples = [
        {
            "name": "FastAPI",
            "url": "https://github.com/tiangolo/fastapi",
            "description": "Modern, fast web framework for building APIs with Python"
        },
        {
            "name": "React",
            "url": "https://github.com/facebook/react",
            "description": "A JavaScript library for building user interfaces"
        },
        {
            "name": "TensorFlow",
            "url": "https://github.com/tensorflow/tensorflow",
            "description": "Open source machine learning framework"
        },
        {
            "name": "Vue.js",
            "url": "https://github.com/vuejs/vue",
            "description": "Progressive JavaScript framework for building UIs"
        },
        {
            "name": "Django",
            "url": "https://github.com/django/django",
            "description": "High-level Python web framework"
        }
    ]
    
    print("📚 Example Repositories for Demo:")
    print("=" * 60)
    
    for i, repo in enumerate(examples, 1):
        print(f"{i}. {repo['name']}")
        print(f"   URL: {repo['url']}")
        print(f"   Description: {repo['description']}")
        print()
    
    return examples


def show_usage_examples():
    """Show usage examples with different languages."""
    print("🚀 Usage Examples:")
    print("=" * 60)
    
    examples = [
        {
            "command": "python main.py --url https://github.com/user/repo",
            "description": "Basic analysis in English"
        },
        {
            "command": "python main.py --url https://github.com/user/repo --lang hi",
            "description": "Analysis in Hindi"
        },
        {
            "command": "python main.py --url https://github.com/user/repo --lang ur",
            "description": "Analysis in Urdu"
        },
        {
            "command": "python main.py --url https://github.com/user/repo --save",
            "description": "Analysis with output saved to file"
        },
        {
            "command": "python main.py --url https://github.com/user/repo --lang hi --save",
            "description": "Hindi analysis with output saved to file"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['command']}")
        print(f"   → {example['description']}")
        print()
    
    print("For more options: python main.py --help")


def show_features():
    """Show the key features of the agent."""
    print("✨ Key Features:")
    print("=" * 60)
    
    features = [
        "🔍 Intelligent Repository Analysis",
        "   • README.md content analysis",
        "   • Project folder structure mapping",
        "   • Key configuration file detection",
        "   • Technology stack identification",
        "",
        "🤖 AI-Powered Summarization",
        "   • OpenAI GPT integration",
        "   • Comprehensive project overview",
        "   • Feature and capability analysis",
        "   • Setup and installation guidance",
        "   • Code structure explanation",
        "   • Improvement suggestions",
        "",
        "🌍 Multi-Language Support",
        "   • English (default)",
        "   • Hindi (हिंदी)",
        "   • Urdu (اردو)",
        "",
        "💾 Output Options",
        "   • Clean CLI display",
        "   • File export capability",
        "   • Structured summary format",
        "",
        "⚡ Performance Features",
        "   • Progress indicators",
        "   • Error handling",
        "   • Rate limit management",
        "   • File size optimization"
    ]
    
    for feature in features:
        print(feature)


def show_installation_steps():
    """Show installation and setup steps."""
    print("\n🔧 Installation & Setup:")
    print("=" * 60)
    
    steps = [
        "1. Clone the repository",
        "2. Navigate to the project directory",
        "3. Run: install.bat (Windows) or create virtual environment manually",
        "4. Activate virtual environment",
        "5. Run: python setup.py",
        "6. Enter your OpenAI API key when prompted",
        "7. Test installation: python test_installation.py",
        "8. Start analyzing: python main.py --url <github-url>"
    ]
    
    for step in steps:
        print(step)


def interactive_demo():
    """Run an interactive demo."""
    print("\n🎮 Interactive Demo Mode:")
    print("=" * 60)
    
    examples = show_example_repositories()
    
    try:
        choice = input("\nSelect a repository to analyze (1-5) or press Enter to skip: ").strip()
        
        if choice and choice.isdigit() and 1 <= int(choice) <= len(examples):
            repo = examples[int(choice) - 1]
            print(f"\n🎯 Selected: {repo['name']}")
            print(f"   URL: {repo['url']}")
            
            # Show the command to run
            print(f"\n💻 Run this command to analyze:")
            print(f"   python main.py --url {repo['url']}")
            
            # Ask about language preference
            lang_choice = input("\nChoose language (en/hi/ur) [default: en]: ").strip().lower()
            if lang_choice in ['hi', 'ur']:
                print(f"   python main.py --url {repo['url']} --lang {lang_choice}")
            
            # Ask about saving
            save_choice = input("\nSave output to file? (y/N): ").strip().lower()
            if save_choice == 'y':
                lang_part = f" --lang {lang_choice}" if lang_choice in ['hi', 'ur'] else ""
                print(f"   python main.py --url {repo['url']}{lang_part} --save")
            
        else:
            print("Demo mode skipped.")
            
    except KeyboardInterrupt:
        print("\n\nDemo interrupted.")
    except Exception as e:
        print(f"\nDemo error: {e}")


def main():
    """Main demo function."""
    show_demo_banner()
    
    while True:
        print("\n📋 Demo Menu:")
        print("1. Show Example Repositories")
        print("2. Show Usage Examples")
        print("3. Show Key Features")
        print("4. Show Installation Steps")
        print("5. Interactive Demo")
        print("6. Exit")
        
        try:
            choice = input("\nSelect an option (1-6): ").strip()
            
            if choice == "1":
                show_example_repositories()
            elif choice == "2":
                show_usage_examples()
            elif choice == "3":
                show_features()
            elif choice == "4":
                show_installation_steps()
            elif choice == "5":
                interactive_demo()
            elif choice == "6":
                print("\n👋 Thanks for trying RepoSummarizerAgent!")
                print("   Happy coding! 🚀")
                break
            else:
                print("❌ Invalid choice. Please select 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
