#!/usr/bin/env python3
"""
GitHelperBot Demo Script
Demonstrates the key features of the Git Helper Bot
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


def demo_typo_correction():
    """Demonstrate typo correction functionality"""
    print("🔍 Typo Correction Demo")
    print("=" * 50)
    
    corrector = CommandCorrector()
    
    # Test cases with common typos
    test_commands = [
        "git cmomit -m 'Initial commit'",
        "git chekout main",
        "git stauts",
        "git pul origin main",
        "git brnch feature/new-feature",
        "git merg feature/new-feature",
        "git rebas -i HEAD~3",
        "git pus --force origin main",
    ]
    
    for cmd in test_commands:
        print(f"\nInput:  {cmd}")
        correction = corrector.correct_command(cmd)
        if correction and correction != cmd:
            print(f"Fixed:  {correction}")
        else:
            print("No typos detected")
    
    print("\n" + "=" * 50)


def demo_command_validation():
    """Demonstrate command validation functionality"""
    print("🛡️  Command Validation Demo")
    print("=" * 50)
    
    executor = CommandExecutor()
    
    # Test safe commands
    safe_commands = [
        "git status",
        "git log --oneline -5",
        "git branch -a",
        "git diff HEAD~1",
        "git show HEAD",
    ]
    
    print("\nSafe Commands:")
    for cmd in safe_commands:
        validation = executor.validate_command(cmd)
        status = "✅" if validation['valid'] and not validation['warning'] else "⚠️"
        print(f"{status} {cmd}")
    
    # Test dangerous commands
    dangerous_commands = [
        "git reset --hard HEAD",
        "git push --force origin main",
        "git clean -fd",
        "git branch -D feature/old",
        "git filter-branch --force",
    ]
    
    print("\nDangerous Commands (Blocked):")
    for cmd in dangerous_commands:
        validation = executor.validate_command(cmd)
        if validation['warning']:
            print(f"🚫 {cmd} - {validation['warning']}")
        else:
            print(f"❓ {cmd} - No warning (unexpected)")
    
    print("\n" + "=" * 50)


def demo_file_generation():
    """Demonstrate file generation functionality"""
    print("📄 File Generation Demo")
    print("=" * 50)
    
    generator = FileGenerator()
    
    # Show available templates
    templates = generator.get_available_templates()
    print(f"\nAvailable .gitignore templates: {', '.join(templates)}")
    
    # Generate sample files
    print("\nGenerating sample files...")
    
    # Create a temporary directory for demo
    demo_dir = Path("demo_output")
    demo_dir.mkdir(exist_ok=True)
    
    original_cwd = os.getcwd()
    os.chdir(demo_dir)
    
    try:
        # Generate Python .gitignore
        success = generator.generate_gitignore('python')
        if success:
            print("✅ Generated Python .gitignore")
        
        # Generate README
        success = generator.generate_readme("GitHelperBot Demo Project")
        if success:
            print("✅ Generated README.md")
        
        # Show file contents
        print("\nGenerated .gitignore (first 10 lines):")
        with open('.gitignore', 'r') as f:
            lines = f.readlines()[:10]
            for line in lines:
                print(f"  {line.rstrip()}")
        
        print("\nGenerated README.md (first 10 lines):")
        with open('README.md', 'r') as f:
            lines = f.readlines()[:10]
            for line in lines:
                print(f"  {line.rstrip()}")
    
    finally:
        os.chdir(original_cwd)
        # Clean up demo directory
        import shutil
        if demo_dir.exists():
            shutil.rmtree(demo_dir)
    
    print("\n" + "=" * 50)


def demo_cli_interface():
    """Demonstrate CLI interface functionality"""
    print("🖥️  CLI Interface Demo")
    print("=" * 50)
    
    cli = CLIInterface()
    
    # Show different message types
    cli.print_success("This is a success message")
    cli.print_warning("This is a warning message")
    cli.print_error("This is an error message")
    cli.print_info("This is an info message")
    
    # Show markdown rendering
    markdown_content = """
# Sample Markdown

This is **bold text** and this is *italic text*.

```bash
git status
git add .
git commit -m "Sample commit"
```

- List item 1
- List item 2
- List item 3
    """
    
    print("\nMarkdown rendering:")
    cli.print_markdown(markdown_content)
    
    print("\n" + "=" * 50)


def main():
    """Run all demos"""
    print("🤖 GitHelperBot Feature Demo")
    print("=" * 60)
    print("This demo showcases the key features of GitHelperBot")
    print("without requiring an OpenAI API key.")
    print("=" * 60)
    
    try:
        demo_typo_correction()
        demo_command_validation()
        demo_file_generation()
        demo_cli_interface()
        
        print("\n🎉 Demo completed successfully!")
        print("\nTo use GitHelperBot with full AI features:")
        print("1. Set up your OpenAI API key in .env file")
        print("2. Run: python agent.py --interactive")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
