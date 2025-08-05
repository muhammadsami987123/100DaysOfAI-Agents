#!/usr/bin/env python3
"""
Quick speech fix script for TranslatorAgent
"""

import sys
import platform
from colorama import init, Fore, Style

# Initialize colorama
init()

def print_colored(text: str, color: str = Fore.WHITE, style: str = ""):
    """Print colored text"""
    print(f"{color}{style}{text}{Style.RESET_ALL}")

def quick_speech_test():
    """Quick speech test"""
    print_colored("🔊 Quick Speech Test", Fore.CYAN, Style.BRIGHT)
    print_colored("=" * 30, Fore.CYAN)
    
    try:
        from voice_service import VoiceService
        
        voice_service = VoiceService()
        
        # Test speech
        test_text = "Hello, this is a test."
        print_colored(f"Speaking: '{test_text}'", Fore.YELLOW)
        
        result = voice_service.speak_text(test_text, "en")
        
        if result["success"]:
            print_colored("✅ Speech test successful! You should hear audio.", Fore.GREEN)
            return True
        else:
            print_colored(f"❌ Speech test failed: {result['error']}", Fore.RED)
            return False
            
    except Exception as e:
        print_colored(f"❌ Speech test error: {str(e)}", Fore.RED)
        return False

def show_quick_fixes():
    """Show quick fixes for common speech issues"""
    print_colored("\n🔧 Quick Fixes:", Fore.CYAN)
    
    system = platform.system().lower()
    
    if system == "windows":
        print_colored("Windows fixes:", Fore.YELLOW)
        print_colored("   1. Check Windows volume (bottom right taskbar)", Fore.CYAN)
        print_colored("   2. Right-click speaker icon > Open Sound settings", Fore.CYAN)
        print_colored("   3. Test speakers in Sound settings", Fore.CYAN)
        print_colored("   4. Try: python -c \"import pyttsx3; pyttsx3.init().say('test')\"", Fore.CYAN)
    
    elif system == "darwin":  # macOS
        print_colored("macOS fixes:", Fore.YELLOW)
        print_colored("   1. Check System Preferences > Sound", Fore.CYAN)
        print_colored("   2. Test audio in Sound settings", Fore.CYAN)
        print_colored("   3. Try: afplay /System/Library/Sounds/Glass.aiff", Fore.CYAN)
    
    else:  # Linux
        print_colored("Linux fixes:", Fore.YELLOW)
        print_colored("   1. Install espeak: sudo apt-get install espeak", Fore.CYAN)
        print_colored("   2. Test: speaker-test -t wav -c 1 -l 1", Fore.CYAN)
        print_colored("   3. Check: pactl list sinks", Fore.CYAN)
    
    print_colored("\nGeneral fixes:", Fore.YELLOW)
    print_colored("   1. Check if speakers/headphones are connected", Fore.CYAN)
    print_colored("   2. Try different audio output device", Fore.CYAN)
    print_colored("   3. Restart the application", Fore.CYAN)
    print_colored("   4. Run: python test_voice.py", Fore.CYAN)

def main():
    """Main function"""
    print_colored("🎯 Quick Speech Fix", Fore.CYAN, Style.BRIGHT)
    print_colored("=" * 30, Fore.CYAN)
    
    # Run quick test
    success = quick_speech_test()
    
    if success:
        print_colored("\n🎉 Speech is working! Try the web interface now.", Fore.GREEN)
        print_colored("   python main.py --web", Fore.CYAN)
    else:
        print_colored("\n❌ Speech is not working. Try these fixes:", Fore.RED)
        show_quick_fixes()
        
        print_colored("\n💡 For detailed diagnostics, run:", Fore.YELLOW)
        print_colored("   python test_voice.py", Fore.CYAN)

if __name__ == "__main__":
    main() 