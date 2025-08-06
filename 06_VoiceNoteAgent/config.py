#!/usr/bin/env python3
"""
Configuration and setup instructions for VoiceNoteAgent

This module contains setup instructions and configuration settings
for the VoiceNoteAgent voice note-taking system.

Author: Muhammad Sami Asghar Mughal
"""

import os
import sys
from colorama import Fore, Style

def setup_instructions():
    """Display setup instructions for VoiceNoteAgent."""
    print(f"{Fore.CYAN}🤖 VoiceNoteAgent Setup Instructions")
    print("=" * 60)
    print()
    
    print(f"{Fore.YELLOW}📋 Prerequisites:")
    print(f"{Fore.WHITE}   1. Python 3.7 or higher")
    print(f"{Fore.WHITE}   2. Working microphone")
    print(f"{Fore.WHITE}   3. Speakers or headphones (for TTS playback)")
    print()
    
    print(f"{Fore.YELLOW}🔧 Installation Steps:")
    print(f"{Fore.WHITE}   1. Install Python dependencies:")
    print(f"{Fore.GREEN}      pip install -r requirements.txt")
    print()
    
    print(f"{Fore.WHITE}   2. For Windows users (if PyAudio fails):")
    print(f"{Fore.GREEN}      pip install pipwin")
    print(f"{Fore.GREEN}      pipwin install pyaudio")
    print()
    
    print(f"{Fore.WHITE}   3. For macOS users:")
    print(f"{Fore.GREEN}      brew install portaudio")
    print(f"{Fore.GREEN}      pip install pyaudio")
    print()
    
    print(f"{Fore.WHITE}   4. For Linux users:")
    print(f"{Fore.GREEN}      sudo apt-get install python3-pyaudio portaudio19-dev")
    print(f"{Fore.GREEN}      pip install pyaudio")
    print()
    
    print(f"{Fore.YELLOW}🎤 Microphone Setup:")
    print(f"{Fore.WHITE}   - Ensure your microphone is connected and working")
    print(f"{Fore.WHITE}   - Test microphone in your system settings")
    print(f"{Fore.WHITE}   - The agent will calibrate for ambient noise on startup")
    print()
    
    print(f"{Fore.YELLOW}🔊 Text-to-Speech Setup:")
    print(f"{Fore.WHITE}   - Windows: Uses built-in SAPI voices")
    print(f"{Fore.WHITE}   - macOS: Uses built-in NSSpeechSynthesizer")
    print(f"{Fore.WHITE}   - Linux: Requires espeak or festival")
    print()
    
    print(f"{Fore.YELLOW}🌐 Internet Requirements:")
    print(f"{Fore.WHITE}   - Google Speech Recognition: Requires internet")
    print(f"{Fore.WHITE}   - Sphinx (offline): No internet required")
    print(f"{Fore.WHITE}   - The agent will try both methods")
    print()
    
    print(f"{Fore.YELLOW}🚀 Running the Agent:")
    print(f"{Fore.GREEN}   python main.py")
    print()
    
    print(f"{Fore.YELLOW}📁 File Storage:")
    print(f"{Fore.WHITE}   - Notes are saved in 'voice_notes.json'")
    print(f"{Fore.WHITE}   - Individual TXT files in 'voice_notes/' directory")
    print(f"{Fore.WHITE}   - All data is stored locally")
    print()
    
    print(f"{Fore.CYAN}💡 Tips for Best Results:")
    print(f"{Fore.WHITE}   - Speak clearly and at a normal pace")
    print(f"{Fore.WHITE}   - Minimize background noise")
    print(f"{Fore.WHITE}   - Use 10-30 second recordings for best accuracy")
    print(f"{Fore.WHITE}   - Test with short phrases first")
    print()
    
    print(f"{Fore.GREEN}✅ Setup complete! Run 'python main.py' to start.")
    print("=" * 60)

def check_dependencies():
    """Check if all required dependencies are installed."""
    missing_deps = []
    
    try:
        import speech_recognition
        print(f"{Fore.GREEN}✅ SpeechRecognition installed")
    except ImportError:
        missing_deps.append("SpeechRecognition")
        print(f"{Fore.RED}❌ SpeechRecognition not installed")
    
    try:
        import pyttsx3
        print(f"{Fore.GREEN}✅ pyttsx3 installed")
    except ImportError:
        missing_deps.append("pyttsx3")
        print(f"{Fore.RED}❌ pyttsx3 not installed")
    
    try:
        import pyaudio
        print(f"{Fore.GREEN}✅ PyAudio installed")
    except ImportError:
        missing_deps.append("PyAudio")
        print(f"{Fore.RED}❌ PyAudio not installed")
    
    try:
        import colorama
        print(f"{Fore.GREEN}✅ colorama installed")
    except ImportError:
        missing_deps.append("colorama")
        print(f"{Fore.RED}❌ colorama not installed")
    
    # Optional: pocketsphinx for offline recognition
    try:
        import pocketsphinx
        print(f"{Fore.GREEN}✅ pocketsphinx installed (offline recognition available)")
    except ImportError:
        print(f"{Fore.YELLOW}⚠️  pocketsphinx not installed (offline recognition not available)")
    
    if missing_deps:
        print(f"\n{Fore.RED}❌ Missing dependencies: {', '.join(missing_deps)}")
        print(f"{Fore.YELLOW}💡 Run: pip install -r requirements.txt")
        return False
    
    print(f"\n{Fore.GREEN}✅ All required dependencies are installed!")
    return True

def check_microphone():
    """Check if microphone is available."""
    try:
        import speech_recognition as sr
        mic = sr.Microphone()
        print(f"{Fore.GREEN}✅ Microphone detected")
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Microphone not available: {e}")
        return False

def check_tts():
    """Check if text-to-speech is working."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if voices:
            print(f"{Fore.GREEN}✅ Text-to-speech available ({len(voices)} voices)")
            return True
        else:
            print(f"{Fore.YELLOW}⚠️  No TTS voices found")
            return False
    except Exception as e:
        print(f"{Fore.RED}❌ Text-to-speech not available: {e}")
        return False

def run_system_check():
    """Run a complete system check."""
    print(f"{Fore.CYAN}🔍 VoiceNoteAgent System Check")
    print("=" * 40)
    
    deps_ok = check_dependencies()
    mic_ok = check_microphone()
    tts_ok = check_tts()
    
    print("\n" + "=" * 40)
    if deps_ok and mic_ok and tts_ok:
        print(f"{Fore.GREEN}✅ System check passed! Ready to run VoiceNoteAgent.")
        return True
    else:
        print(f"{Fore.RED}❌ System check failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        run_system_check()
    else:
        setup_instructions() 