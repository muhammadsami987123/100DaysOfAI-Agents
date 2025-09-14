#!/usr/bin/env python3
"""
Simple startup script for JarvisMouseControl
Handles common issues and provides easy startup
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'speech_recognition',
        'pyttsx3', 
        'pyautogui',
        'openai'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}: OK")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}: Missing")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("💡 Install with: pip install -r requirements.txt")
        return False
    
    return True

def check_microphone():
    """Check microphone availability"""
    try:
        import speech_recognition as sr
        mic_list = sr.Microphone.list_microphone_names()
        if mic_list:
            print(f"✅ Microphones found: {len(mic_list)}")
            return True
        else:
            print("⚠️  No microphones detected")
            return False
    except Exception as e:
        print(f"⚠️  Microphone check failed: {e}")
        return False

def main():
    """Main startup function"""
    print("=" * 60)
    print("🚀 JarvisMouseControl - Startup Check")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Check microphone
    mic_available = check_microphone()
    
    print("\n" + "=" * 60)
    print("🎯 Starting JarvisMouseControl...")
    print("=" * 60)
    
    # Import and run main
    try:
        from main import main as main_func
        return main_func()
    except Exception as e:
        print(f"❌ Failed to start: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
