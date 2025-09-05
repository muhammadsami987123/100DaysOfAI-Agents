"""
Test file for GitHelperBot commands
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.command_corrector import CommandCorrector
from core.command_executor import CommandExecutor
from utils.file_generator import FileGenerator


def test_command_corrector():
    """Test command corrector functionality"""
    print("Testing Command Corrector...")
    
    corrector = CommandCorrector()
    
    # Test cases
    test_cases = [
        ("git cmomit -m 'test'", "git commit -m 'test'"),
        ("git chekout main", "git checkout main"),
        ("git stauts", "git status"),
        ("git pul origin main", "git pull origin main"),
        ("git pus origin main", "git push origin main"),
        ("git brnch", "git branch"),
        ("git merg feature", "git merge feature"),
        ("git rebas -i HEAD~3", "git rebase -i HEAD~3"),
    ]
    
    for input_cmd, expected in test_cases:
        result = corrector.correct_command(input_cmd)
        if result == expected:
            print(f"✅ {input_cmd} -> {result}")
        else:
            print(f"❌ {input_cmd} -> {result} (expected: {expected})")
    
    print()


def test_command_executor():
    """Test command executor functionality"""
    print("Testing Command Executor...")
    
    executor = CommandExecutor()
    
    # Test safe commands
    safe_commands = [
        "git --version",
        "git status",
        "git log --oneline -5",
        "git branch",
    ]
    
    for cmd in safe_commands:
        validation = executor.validate_command(cmd)
        if validation['valid']:
            print(f"✅ {cmd} - Valid")
        else:
            print(f"❌ {cmd} - Invalid: {validation['error']}")
    
    # Test dangerous commands
    dangerous_commands = [
        "git reset --hard HEAD",
        "git push --force",
        "git clean -fd",
    ]
    
    for cmd in dangerous_commands:
        validation = executor.validate_command(cmd)
        if validation['warning']:
            print(f"⚠️  {cmd} - Warning: {validation['warning']}")
        else:
            print(f"❌ {cmd} - Should have warning")
    
    print()


def test_file_generator():
    """Test file generator functionality"""
    print("Testing File Generator...")
    
    generator = FileGenerator()
    
    # Test available templates
    templates = generator.get_available_templates()
    print(f"Available templates: {templates}")
    
    # Test .gitignore generation
    success = generator.generate_gitignore('python')
    if success:
        print("✅ Python .gitignore generated")
    else:
        print("❌ Failed to generate .gitignore")
    
    # Test README generation
    success = generator.generate_readme("Test Project")
    if success:
        print("✅ README.md generated")
    else:
        print("❌ Failed to generate README.md")
    
    print()


def main():
    """Run all tests"""
    print("🧪 Running GitHelperBot Tests\n")
    
    test_command_corrector()
    test_command_executor()
    test_file_generator()
    
    print("✅ All tests completed!")


if __name__ == "__main__":
    main()
