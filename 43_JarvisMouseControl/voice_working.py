#!/usr/bin/env python3
"""
Working Voice Demo for JarvisMouseControl
Uses the same microphone detection logic that works
"""

import sys
import time
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import CONFIG
from voice_handler import VoiceHandler
from mouse_controller import MouseController
from utils.command_parser import CommandParser
import speech_recognition as sr

class WorkingVoiceDemo:
    """Working voice demo with proven microphone detection"""
    
    def __init__(self, language: str = "en"):
        """Initialize working voice demo"""
        self.language = language
        self.running = False
        
        # Initialize components
        self.mouse_controller = MouseController()
        self.command_parser = CommandParser(language)
        
        # Initialize voice handler
        self.voice_handler = VoiceHandler(language)
        
        print(f"🌍 Language: {CONFIG.LANGUAGE_NAMES.get(language, language)}")
    
    def find_working_microphone(self):
        """Find a working microphone using the proven method"""
        try:
            recognizer = sr.Recognizer()
            mic_list = sr.Microphone.list_microphone_names()
            
            for i, mic_name in enumerate(mic_list):
                try:
                    # Skip output devices
                    if any(keyword in mic_name.lower() for keyword in ['output', 'speaker', 'playback']):
                        continue
                    
                    with sr.Microphone(device_index=i) as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.2)
                        print(f"✅ Found working microphone {i}: {mic_name}")
                        return i
                except:
                    continue
            return None
        except Exception as e:
            print(f"❌ Error finding microphone: {e}")
            return None
    
    def start_demo(self):
        """Start the working voice demo"""
        print("=" * 60)
        print("🎤 JarvisMouseControl - Working Voice Demo")
        print("=" * 60)
        
        # Test components
        if not self._test_components():
            return False
        
        print("\n🎯 Available Commands:")
        print("• 'click' - Left click")
        print("• 'move up' - Move cursor up")
        print("• 'move down' - Move cursor down")
        print("• 'move left' - Move cursor left")
        print("• 'move right' - Move cursor right")
        print("• 'double click' - Double click")
        print("• 'right click' - Right click")
        print("• 'scroll up' - Scroll up")
        print("• 'scroll down' - Scroll down")
        print("• 'stop' - Stop the demo")
        
        print("\n💡 You can:")
        print("1. Speak a command (if microphone is working)")
        print("2. Type a command and press Enter")
        print("3. Type 'quit' to exit")
        
        # Main loop
        self.running = True
        print("\n🎤 Starting continuous voice listening...")
        print("💡 Say 'stop' to exit, or press Ctrl+C to quit")
        
        try:
            while self.running:
                # Try voice command first
                self._try_voice_command()
                
                # Small delay to prevent overwhelming
                time.sleep(0.5)
                    
        except KeyboardInterrupt:
            print("\n🛑 Demo interrupted by user")
        finally:
            self.running = False
        
        return True
    
    def _try_voice_command(self):
        """Try to get a voice command using working microphone detection"""
        working_mic = self.find_working_microphone()
        
        if working_mic is None:
            print("❌ No working microphone found")
            print("💡 Use text input instead")
            return
        
        print(f"🎤 Listening... (mic {working_mic})")
        
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone(device_index=working_mic) as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.1)
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                text = recognizer.recognize_google(audio, language="en-US")
                print(f"🎤 Heard: '{text}'")
                self._process_command(text)
                
        except sr.WaitTimeoutError:
            # No speech detected - this is normal, just continue
            pass
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
        except Exception as e:
            print(f"❌ Voice recognition error: {e}")
    
    def _test_components(self):
        """Test all components"""
        print("\n🧪 Testing components...")
        
        # Test mouse controller
        try:
            pos = self.mouse_controller.get_current_position()
            print(f"✅ Mouse controller: OK (position: {pos})")
        except Exception as e:
            print(f"❌ Mouse controller test failed: {e}")
            return False
        
        # Test command parser
        try:
            result = self.command_parser.parse_command("click")
            if result:
                print("✅ Command parser: OK")
            else:
                print("❌ Command parser test failed")
                return False
        except Exception as e:
            print(f"❌ Command parser test failed: {e}")
            return False
        
        # Test voice handler
        if self.voice_handler.is_tts_available():
            print("✅ Text-to-speech: Available")
        else:
            print("⚠️  Text-to-speech: Not available")
        
        # Test microphone
        working_mic = self.find_working_microphone()
        if working_mic is not None:
            print("✅ Voice recognition: Available")
        else:
            print("⚠️  Voice recognition: Not available")
        
        return True
    
    def _process_command(self, text: str):
        """Process a command (voice or text)"""
        if not text or not text.strip():
            return
        
        # Check for stop command
        if self.command_parser.is_stop_command(text):
            print("🛑 Stop command received")
            self.voice_handler.speak("Stopping demo")
            self.running = False
            return
        
        # Parse the command
        action_data = self.command_parser.parse_command(text)
        
        if not action_data:
            print("❌ Command not recognized. Try: click, move up, move down, etc.")
            if self.voice_handler.is_tts_available():
                self.voice_handler.speak("Command not recognized. Please try again.")
            return
        
        # Show recognized command
        print(f"✅ Command recognized: {action_data['action']}")
        if self.voice_handler.is_tts_available():
            self.voice_handler.speak(f"Executing {action_data['action']}")
        
        # Execute the action
        success = self.mouse_controller.execute_action(action_data)
        
        if success:
            print(f"🖱️  Action executed: {action_data['action']}")
            if self.voice_handler.is_tts_available():
                self.voice_handler.speak("Action completed")
        else:
            print("❌ Action failed")
            if self.voice_handler.is_tts_available():
                self.voice_handler.speak("Action failed")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="JarvisMouseControl Working Voice Demo")
    parser.add_argument("--language", "-l", choices=["en", "ur", "hi"], default="en", 
                       help="Language for voice commands")
    
    args = parser.parse_args()
    
    try:
        demo = WorkingVoiceDemo(args.language)
        demo.start_demo()
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    finally:
        print("\n👋 Demo completed. Goodbye!")

if __name__ == "__main__":
    main()
