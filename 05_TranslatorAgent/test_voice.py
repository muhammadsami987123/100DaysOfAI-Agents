#!/usr/bin/env python3
"""
Voice diagnostic script for TranslatorAgent
Helps identify and fix speech-related issues
"""

import sys
import os
import platform
import subprocess
from colorama import init, Fore, Style

# Initialize colorama
init()

def print_colored(text: str, color: str = Fore.WHITE, style: str = ""):
    """Print colored text"""
    print(f"{color}{style}{text}{Style.RESET_ALL}")

def test_system_audio():
    """Test basic system audio functionality"""
    print_colored("🔊 Testing System Audio...", Fore.CYAN)
    
    system = platform.system()
    print_colored(f"Platform: {system}", Fore.YELLOW)
    
    if system == "Windows":
        # Test Windows audio
        try:
            # Try to play a test sound using PowerShell
            test_command = 'powershell -Command "[console]::beep(800,500)"'
            subprocess.run(test_command, shell=True, check=True)
            print_colored("✅ Windows audio test successful", Fore.GREEN)
        except:
            print_colored("❌ Windows audio test failed", Fore.RED)
    
    elif system == "Darwin":  # macOS
        try:
            # Test macOS audio
            test_command = 'afplay /System/Library/Sounds/Glass.aiff'
            subprocess.run(test_command, shell=True, check=True)
            print_colored("✅ macOS audio test successful", Fore.GREEN)
        except:
            print_colored("❌ macOS audio test failed", Fore.RED)
    
    else:  # Linux
        try:
            # Test Linux audio
            test_command = 'speaker-test -t wav -c 1 -l 1'
            subprocess.run(test_command, shell=True, check=True, timeout=3)
            print_colored("✅ Linux audio test successful", Fore.GREEN)
        except:
            print_colored("❌ Linux audio test failed", Fore.RED)

def test_pyttsx3():
    """Test pyttsx3 TTS engine"""
    print_colored("\n🗣️  Testing pyttsx3 TTS Engine...", Fore.CYAN)
    
    try:
        import pyttsx3
        
        # Try to initialize
        engine = pyttsx3.init()
        print_colored("✅ pyttsx3 initialized", Fore.GREEN)
        
        # Get properties
        rate = engine.getProperty('rate')
        volume = engine.getProperty('volume')
        voices = engine.getProperty('voices')
        
        print_colored(f"   Rate: {rate}", Fore.CYAN)
        print_colored(f"   Volume: {volume}", Fore.CYAN)
        print_colored(f"   Voices: {len(voices) if voices else 0}", Fore.CYAN)
        
        if voices:
            print_colored("   Available voices:", Fore.CYAN)
            for i, voice in enumerate(voices[:3]):  # Show first 3
                print_colored(f"     {i+1}. {voice.name} ({voice.id})", Fore.CYAN)
        
        # Test speech
        print_colored("   Testing speech...", Fore.YELLOW)
        engine.say("Test speech")
        engine.runAndWait()
        print_colored("✅ Speech test successful", Fore.GREEN)
        
        return True
        
    except Exception as e:
        print_colored(f"❌ pyttsx3 test failed: {str(e)}", Fore.RED)
        return False

def test_speech_recognition():
    """Test speech recognition"""
    print_colored("\n🎤 Testing Speech Recognition...", Fore.CYAN)
    
    try:
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        print_colored("✅ Speech recognition initialized", Fore.GREEN)
        
        # Test microphone
        try:
            with sr.Microphone() as source:
                print_colored("✅ Microphone available", Fore.GREEN)
        except Exception as e:
            print_colored(f"❌ Microphone error: {str(e)}", Fore.RED)
            return False
        
        return True
        
    except Exception as e:
        print_colored(f"❌ Speech recognition test failed: {str(e)}", Fore.RED)
        return False

def test_voice_service():
    """Test the VoiceService class"""
    print_colored("\n🤖 Testing VoiceService...", Fore.CYAN)
    
    try:
        from voice_service import VoiceService
        
        voice_service = VoiceService()
        print_colored("✅ VoiceService initialized", Fore.GREEN)
        
        # Health check
        health = voice_service.health_check()
        print_colored(f"   Status: {health['status']}", Fore.CYAN)
        print_colored(f"   TTS: {health['tts_details']}", Fore.CYAN)
        print_colored(f"   Microphone: {health['microphone_details']}", Fore.CYAN)
        print_colored(f"   Speech Recognition: {health['speech_recognition_details']}", Fore.CYAN)
        
        # Test speech
        if health['tts_available']:
            print_colored("   Testing speech...", Fore.YELLOW)
            result = voice_service.speak_text("Hello world", "en")
            if result["success"]:
                print_colored("✅ Speech test successful", Fore.GREEN)
            else:
                print_colored(f"❌ Speech test failed: {result['error']}", Fore.RED)
        
        return health['status'] == 'healthy'
        
    except Exception as e:
        print_colored(f"❌ VoiceService test failed: {str(e)}", Fore.RED)
        return False

def show_troubleshooting_tips():
    """Show troubleshooting tips"""
    print_colored("\n🔧 Troubleshooting Tips:", Fore.CYAN)
    
    system = platform.system().lower()
    
    if system == "windows":
        print_colored("Windows-specific tips:", Fore.YELLOW)
        print_colored("   1. Check Windows Audio settings", Fore.CYAN)
        print_colored("   2. Ensure speakers/headphones are connected", Fore.CYAN)
        print_colored("   3. Try running as administrator", Fore.CYAN)
        print_colored("   4. Install Windows Media Player", Fore.CYAN)
        print_colored("   5. Check microphone permissions in Settings > Privacy > Microphone", Fore.CYAN)
    
    elif system == "darwin":  # macOS
        print_colored("macOS-specific tips:", Fore.YELLOW)
        print_colored("   1. Check System Preferences > Sound", Fore.CYAN)
        print_colored("   2. Ensure microphone permissions", Fore.CYAN)
        print_colored("   3. Try using external speakers/headphones", Fore.CYAN)
        print_colored("   4. Check Audio MIDI Setup utility", Fore.CYAN)
    
    else:  # Linux
        print_colored("Linux-specific tips:", Fore.YELLOW)
        print_colored("   1. Install espeak: sudo apt-get install espeak", Fore.CYAN)
        print_colored("   2. Check ALSA/PulseAudio configuration", Fore.CYAN)
        print_colored("   3. Try: sudo apt-get install python3-pyaudio", Fore.CYAN)
        print_colored("   4. Check microphone permissions", Fore.CYAN)
        print_colored("   5. Test with: speaker-test -t wav", Fore.CYAN)
    
    print_colored("\nGeneral tips:", Fore.YELLOW)
    print_colored("   1. Check system volume and mute settings", Fore.CYAN)
    print_colored("   2. Try different audio output devices", Fore.CYAN)
    print_colored("   3. Update audio drivers", Fore.CYAN)
    print_colored("   4. Restart the application", Fore.CYAN)
    print_colored("   5. Test with a simple text first", Fore.CYAN)

def test_simple_speech():
    """Test simple speech functionality"""
    print_colored("\n🎯 Testing Simple Speech...", Fore.CYAN)
    
    try:
        from voice_service import VoiceService
        
        voice_service = VoiceService()
        
        # Test with a simple text
        test_text = "Hello, this is a test."
        print_colored(f"Speaking: '{test_text}'", Fore.YELLOW)
        
        result = voice_service.speak_text(test_text, "en")
        
        if result["success"]:
            print_colored("✅ Simple speech test successful", Fore.GREEN)
            return True
        else:
            print_colored(f"❌ Simple speech test failed: {result['error']}", Fore.RED)
            return False
            
    except Exception as e:
        print_colored(f"❌ Simple speech test error: {str(e)}", Fore.RED)
        return False

def main():
    """Run all voice diagnostics"""
    print_colored("🔍 Voice Diagnostic Tool", Fore.CYAN, Style.BRIGHT)
    print_colored("=" * 50, Fore.CYAN)
    
    tests = [
        ("System Audio", test_system_audio),
        ("pyttsx3 TTS Engine", test_pyttsx3),
        ("Speech Recognition", test_speech_recognition),
        ("VoiceService", test_voice_service),
        ("Simple Speech", test_simple_speech)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print_colored(f"❌ {test_name} failed with exception: {str(e)}", Fore.RED)
    
    print_colored("\n" + "=" * 50, Fore.CYAN)
    print_colored(f"📊 Test Results: {passed}/{total} passed", Fore.CYAN)
    
    if passed == total:
        print_colored("🎉 All voice tests passed! Speech should work.", Fore.GREEN)
    else:
        print_colored("❌ Some voice tests failed. Check the issues above.", Fore.RED)
        show_troubleshooting_tips()
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 