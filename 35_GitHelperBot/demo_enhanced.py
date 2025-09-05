#!/usr/bin/env python3
"""
GitHelperBot Enhanced UI Demo
Demonstrates the improved UI and suggestion features
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.command_corrector import CommandCorrector
from core.command_executor import CommandExecutor
from utils.file_generator import FileGenerator
from utils.cli_interface import CLIInterface
from utils.command_history import CommandHistory


def demo_enhanced_ui():
    """Demonstrate enhanced UI features"""
    print("🎨 Enhanced UI Demo")
    print("=" * 60)
    
    cli = CLIInterface()
    
    # Show the new welcome screen
    cli.print_welcome()
    
    print("\n" + "=" * 60)
    print("✨ New Features Demonstrated:")
    print("• Beautiful welcome screen with feature cards")
    print("• Interactive suggestion menus")
    print("• Command history and favorites")
    print("• Quick action shortcuts")
    print("• Enhanced error handling")
    print("• Statistics and usage tracking")
    print("=" * 60)


def demo_suggestion_system():
    """Demonstrate suggestion system"""
    print("\n🔍 Suggestion System Demo")
    print("=" * 50)
    
    corrector = CommandCorrector()
    cli = CLIInterface()
    
    # Test typo correction with suggestions
    test_commands = [
        "git cmomit -m 'test'",
        "git chekout main",
        "git stauts",
        "git pul origin main"
    ]
    
    for cmd in test_commands:
        print(f"\nInput: {cmd}")
        correction = corrector.correct_command(cmd)
        
        if correction and correction != cmd:
            suggestions = [correction]
            additional = corrector.get_suggestions(cmd, 2)
            suggestions.extend(additional)
            
            print("Suggestions found:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")
        else:
            print("No typos detected")


def demo_command_history():
    """Demonstrate command history features"""
    print("\n📜 Command History Demo")
    print("=" * 50)
    
    history = CommandHistory("demo_history.json")
    
    # Add some sample commands
    sample_commands = [
        ("git status", True, 0.5),
        ("git add .", True, 0.3),
        ("git commit -m 'Initial commit'", True, 1.2),
        ("git push origin main", True, 2.1),
        ("git pull origin main", True, 1.8),
        ("git branch", True, 0.4),
        ("git log --oneline", True, 0.6),
        ("git checkout -b feature", True, 0.7),
        ("git merge feature", False, 0.2),  # Failed command
        ("git stash", True, 0.3)
    ]
    
    print("Adding sample commands to history...")
    for cmd, success, exec_time in sample_commands:
        history.add_command(cmd, success, exec_time)
    
    # Show statistics
    stats = history.get_command_stats()
    print(f"\nCommand Statistics:")
    print(f"Total commands: {stats['total']}")
    print(f"Success rate: {stats['success_rate']}%")
    print(f"Most used commands:")
    for cmd, count in stats['most_used']:
        print(f"  {cmd}: {count} times")
    
    # Show recent commands
    recent = history.get_recent_commands(5)
    print(f"\nRecent commands:")
    for cmd in recent:
        print(f"  • {cmd}")
    
    # Clean up
    if os.path.exists("demo_history.json"):
        os.remove("demo_history.json")


def demo_file_generation():
    """Demonstrate enhanced file generation"""
    print("\n📄 File Generation Demo")
    print("=" * 50)
    
    generator = FileGenerator()
    cli = CLIInterface()
    
    # Show available templates
    templates = generator.get_available_templates()
    print(f"Available .gitignore templates: {', '.join(templates)}")
    
    # Create demo directory
    demo_dir = Path("demo_output_enhanced")
    demo_dir.mkdir(exist_ok=True)
    
    original_cwd = os.getcwd()
    os.chdir(demo_dir)
    
    try:
        # Generate different types of files
        print("\nGenerating files...")
        
        # Python .gitignore
        success = generator.generate_gitignore('python')
        if success:
            print("✅ Generated Python .gitignore")
        
        # Node.js .gitignore
        success = generator.generate_gitignore('nodejs')
        if success:
            print("✅ Generated Node.js .gitignore")
        
        # README
        success = generator.generate_readme("Enhanced GitHelperBot Demo")
        if success:
            print("✅ Generated README.md")
        
        # Show file contents
        print("\nGenerated files:")
        for file_path in demo_dir.glob("*"):
            print(f"  📄 {file_path.name}")
    
    finally:
        os.chdir(original_cwd)
        # Clean up
        import shutil
        if demo_dir.exists():
            shutil.rmtree(demo_dir)


def demo_quick_actions():
    """Demonstrate quick actions menu"""
    print("\n⚡ Quick Actions Demo")
    print("=" * 50)
    
    cli = CLIInterface()
    
    # Show quick actions menu
    print("Quick Actions Menu:")
    actions = [
        ("1", "git status", "Check repository status"),
        ("2", "git add .", "Stage all changes"),
        ("3", "git commit -m \"message\"", "Commit changes"),
        ("4", "git push origin main", "Push to remote"),
        ("5", "git pull origin main", "Pull from remote"),
        ("6", "git branch", "List branches"),
        ("7", "git log --oneline -5", "Show recent commits"),
        ("8", "generate gitignore", "Create .gitignore file"),
        ("9", "generate readme", "Create README.md file"),
        ("h", "history", "Show command history"),
        ("f", "favorites", "Show favorite commands"),
        ("0", "help", "Show help information")
    ]
    
    from rich.table import Table
    from rich.box import ROUNDED
    table = Table(show_header=True, box=ROUNDED, padding=(0, 1))
    table.add_column("Key", style="cyan", width=3)
    table.add_column("Command", style="yellow", width=40)
    table.add_column("Description", style="dim white", width=30)
    
    for key, cmd, desc in actions:
        table.add_row(key, cmd, desc)
    
    cli.console.print(table)


def main():
    """Run all enhanced demos"""
    print("🚀 GitHelperBot Enhanced Features Demo")
    print("=" * 80)
    print("This demo showcases the improved UI and new features:")
    print("• Enhanced visual design with tables and panels")
    print("• Interactive suggestion menus")
    print("• Command history and favorites system")
    print("• Quick action shortcuts")
    print("• Better error handling and user feedback")
    print("=" * 80)
    
    try:
        demo_enhanced_ui()
        demo_suggestion_system()
        demo_command_history()
        demo_file_generation()
        demo_quick_actions()
        
        print("\n🎉 Enhanced Demo completed successfully!")
        print("\nTo use the enhanced GitHelperBot:")
        print("1. Run: python agent.py --menu (for main menu)")
        print("2. Run: python agent.py --interactive (for quick actions)")
        print("3. Run: python agent.py 'command' (for single command)")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
