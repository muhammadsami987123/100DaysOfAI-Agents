#!/usr/bin/env python3
"""
Test script to verify DesktopAgentWrapper installation
"""

import sys
import importlib
import os
from pathlib import Path

def test_python_version():
    """Test if Python version is compatible"""
    print("🐍 Testing Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - OK")
        return True

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'customtkinter',
        'PIL',
        'requests',
        'dotenv',
        'openai',
        'google.generativeai',
        'rich',
        'pydantic'
    ]
    
    print("\n🔍 Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    return failed_imports

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")
    required_files = [
        'desktop_gui.py',
        'config.py',
        'main.py',
        'requirements.txt',
        'agents/__init__.py',
        'agents/agent_base.py',
        'agents/article_rewriter_wrapper.py',
        'agents/story_writer_wrapper.py',
        'agents/prompt_improver_wrapper.py',
        'utils/__init__.py',
        'utils/export_utils.py',
        'utils/session_manager.py',
        'utils/theme_manager.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ Missing: {file_path}")
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    return missing_files

def test_config():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    try:
        from config import Config
        print("✅ Configuration module imported")
        
        # Test theme configuration
        themes = Config.get_available_themes()
        if themes and len(themes) > 0:
            print(f"✅ Themes configured: {len(themes)} available")
        else:
            print("❌ No themes configured")
            return False
        
        # Test agent types
        agent_types = Config.AGENT_TYPES
        if agent_types and len(agent_types) > 0:
            print(f"✅ Agent types configured: {len(agent_types)} available")
        else:
            print("❌ No agent types configured")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_agent_wrappers():
    """Test agent wrapper imports"""
    print("\n🤖 Testing agent wrappers...")
    try:
        from agents import (
            BaseAgent,
            ArticleRewriterWrapper,
            StoryWriterWrapper,
            PromptImproverWrapper
        )
        print("✅ Agent wrapper modules imported")
        
        # Test base agent
        print("✅ BaseAgent class available")
        
        return True
    except Exception as e:
        print(f"❌ Agent wrapper error: {e}")
        return False

def test_desktop_gui():
    """Test desktop GUI module"""
    print("\n🖥️ Testing desktop GUI...")
    try:
        from desktop_gui import DesktopAgentWrapper
        print("✅ DesktopAgentWrapper class imported")
        return True
    except Exception as e:
        print(f"❌ Desktop GUI error: {e}")
        return False

def test_utilities():
    """Test utility modules"""
    print("\n🛠️ Testing utilities...")
    try:
        from utils import ExportManager, SessionManager, ThemeManager
        print("✅ Utility modules imported")
        
        # Test export manager
        export_manager = ExportManager()
        formats = export_manager.get_export_formats()
        print(f"✅ Export formats: {len(formats)} available")
        
        # Test session manager
        session_manager = SessionManager()
        print("✅ Session manager initialized")
        
        # Test theme manager
        theme_manager = ThemeManager()
        themes = theme_manager.get_available_themes()
        print(f"✅ Themes: {len(themes)} available")
        
        return True
    except Exception as e:
        print(f"❌ Utilities error: {e}")
        return False

def test_directories():
    """Test if required directories exist"""
    print("\n📂 Testing directories...")
    required_dirs = [
        'agents',
        'utils',
        'examples',
        'assets',
        'sessions',
        'logs',
        'exports'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            print(f"❌ Missing directory: {dir_path}")
            missing_dirs.append(dir_path)
        else:
            print(f"✅ {dir_path}")
    
    return missing_dirs

def main():
    """Run all tests"""
    print("🖥️ DesktopAgentWrapper - Installation Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test Python version
    if not test_python_version():
        all_tests_passed = False
    
    # Test imports
    failed_imports = test_imports()
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("💡 Run: pip install -r requirements.txt")
        all_tests_passed = False
    
    # Test file structure
    missing_files = test_file_structure()
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        all_tests_passed = False
    
    # Test configuration
    if not test_config():
        all_tests_passed = False
    
    # Test directories
    missing_dirs = test_directories()
    if missing_dirs:
        print(f"\n❌ Missing directories: {', '.join(missing_dirs)}")
        all_tests_passed = False
    
    # Test agent wrappers
    if not test_agent_wrappers():
        all_tests_passed = False
    
    # Test desktop GUI
    if not test_desktop_gui():
        all_tests_passed = False
    
    # Test utilities
    if not test_utilities():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! DesktopAgentWrapper is ready to run.")
        print("\n📋 Next steps:")
        print("1. Set your API keys in .env file")
        print("2. Run: python main.py")
        print("3. Select an agent from the dialog")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
