#!/usr/bin/env python3
"""
🔧 Setup script for BrowserOpenerAgent

Installs dependencies and tests the installation.
"""

import os
import sys
import subprocess
import platform


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python 3.7+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    # Install basic requirements
    if not run_command("pip install -r requirements.txt", "Installing basic requirements"):
        return False
    
    # Try to install PyAudio (optional but recommended)
    system = platform.system().lower()
    
    if system == "windows":
        print("🔄 Attempting to install PyAudio for Windows...")
        if not run_command("pip install pyaudio", "Installing PyAudio"):
            print("⚠️  PyAudio installation failed. Trying pipwin...")
            if not run_command("pip install pipwin", "Installing pipwin"):
                print("⚠️  pipwin installation failed. Voice features may not work.")
            else:
                run_command("pipwin install pyaudio", "Installing PyAudio via pipwin")
    
    elif system == "darwin":  # macOS
        print("🔄 Attempting to install PyAudio for macOS...")
        if not run_command("pip install pyaudio", "Installing PyAudio"):
            print("⚠️  PyAudio installation failed. Try: brew install portaudio && pip install pyaudio")
    
    elif system == "linux":
        print("🔄 Attempting to install PyAudio for Linux...")
        if not run_command("pip install pyaudio", "Installing PyAudio"):
            print("⚠️  PyAudio installation failed. Try: sudo apt-get install python3-pyaudio")
    
    return True


def test_installation():
    """Test if the installation works."""
    print("🧪 Testing installation...")
    
    try:
        # Test importing main modules
        import rich
        print("✅ Rich library imported successfully")
        
        try:
            import speech_recognition as sr
            print("✅ Speech recognition imported successfully")
        except ImportError:
            print("⚠️  Speech recognition not available (voice mode will be disabled)")
        
        try:
            import pyttsx3
            print("✅ Text-to-speech imported successfully")
        except ImportError:
            print("⚠️  Text-to-speech not available (voice feedback will be disabled)")
        
        try:
            import pyaudio
            print("✅ PyAudio imported successfully")
        except ImportError:
            print("⚠️  PyAudio not available (voice input may not work)")
        
        # Test the agent
        print("🔄 Testing BrowserOpenerAgent...")
        if run_command("python test_agent.py", "Running agent tests"):
            print("✅ Agent tests passed!")
        else:
            print("❌ Agent tests failed!")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False


def show_usage_instructions():
    """Show usage instructions."""
    print("\n🎯 Usage Instructions:")
    print("=" * 50)
    print("CLI Mode (default):")
    print("  python main.py")
    print()
    print("Voice Mode:")
    print("  python main.py --voice")
    print()
    print("Show supported sites:")
    print("  python main.py --help-sites")
    print()
    print("Show help:")
    print("  python main.py --help")
    print()
    print("Run tests:")
    print("  python test_agent.py")
    print("=" * 50)


def main():
    """Main setup function."""
    print("🌐 BrowserOpenerAgent Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Dependency installation failed!")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed!")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    show_usage_instructions()
    
    print("\n🚀 You're ready to use BrowserOpenerAgent!")
    print("Try running: python main.py")


if __name__ == "__main__":
    main()
