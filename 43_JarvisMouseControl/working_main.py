#!/usr/bin/env python3
"""
Working version of JarvisMouseControl with fixed voice recognition
"""

import sys
import time
import speech_recognition as sr
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import CONFIG
from mouse_controller import MouseController
from utils.command_parser import CommandParser
from voice_handler import VoiceHandler

class WorkingJarvisMouseControl:
    """Working version of JarvisMouseControl with fixed voice recognition"""
    
    def __init__(self, language: str = "en"):
        """Initialize working JarvisMouseControl agent"""
        self.language = language
        self.running = False
        
        # Initialize components
        self.command_parser = CommandParser(language)
        self.mouse_controller = MouseController()
        self.voice_handler = VoiceHandler(language)
        
        print(f"🌍 Language: {CONFIG.LANGUAGE_NAMES.get(language, language)}")
    
    def find_working_microphone(self):
        """Find a working microphone using the proven method"""
        try:
            recognizer = sr.Recognizer()
            mic_list = sr.Microphone.list_microphone_names()
            
            if not mic_list:
                print("⚠️  No microphones detected")
                return None
            
            print(f"🎤 Found {len(mic_list)} microphone(s)")
            
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
    
    def start(self):
        """Start the working JarvisMouseControl agent"""
        print("=" * 60)
        print("🤖 JarvisMouseControl - Working Version")
        print("=" * 60)
        print(f"🖥️  Screen: {self.mouse_controller.get_screen_size()[0]}x{self.mouse_controller.get_screen_size()[1]}")
        print("=" * 60)
        
        # Test components
        if not self._test_components():
            return False
        
        # Show welcome message
        welcome_msg = self.command_parser.get_feedback_message("welcome")
        print(f"\n{welcome_msg}")
        
        if self.voice_handler.is_tts_available():
            self.voice_handler.speak(welcome_msg)
        
        # Start voice listening
        if not self._start_voice_listening():
            print("⚠️  Voice listening failed. Switching to text-only mode.")
            return self._text_mode()
        
        self.running = True
        
        # Main loop
        try:
            self._main_loop()
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
        finally:
            self.stop()
        
        return True
    
    def _test_components(self) -> bool:
        """Test all components before starting"""
        print("\n🧪 Testing components...")
        
        # Test command parser
        try:
            test_result = self.command_parser.parse_command("click")
            if not test_result:
                print("❌ Command parser test failed")
                return False
            print("✅ Command parser: OK")
        except Exception as e:
            print(f"❌ Command parser test failed: {e}")
            return False
        
        # Test mouse controller
        try:
            pos = self.mouse_controller.get_current_position()
            print(f"✅ Mouse controller: OK (position: {pos})")
        except Exception as e:
            print(f"❌ Mouse controller test failed: {e}")
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
    
    def _start_voice_listening(self) -> bool:
        """Start voice listening with improved microphone detection"""
        try:
            # Find working microphone first
            working_mic = self.find_working_microphone()
            if working_mic is None:
                print("❌ No working microphone found")
                return False
            
            # Start voice listening with the working microphone
            return self.voice_handler.start_listening(self._on_voice_command, working_mic)
        except Exception as e:
            print(f"❌ Error starting voice listening: {e}")
            return False
    
    def _main_loop(self):
        """Main application loop"""
        print("\n🎤 Continuous voice listening active!")
        print("💡 Speak commands or type 'help' for options, 'quit' to exit")
        
        while self.running:
            try:
                # Try voice command first
                self._try_voice_command()
                
                # Small delay to prevent overwhelming
                time.sleep(0.5)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(1)
    
    def _try_voice_command(self):
        """Try to get a voice command using working microphone detection"""
        working_mic = self.find_working_microphone()
        
        if working_mic is None:
            print("❌ No working microphone found")
            return
        
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
    
    def _text_mode(self):
        """Run in text-only mode"""
        print("\n📝 Text input mode")
        print("💡 Type commands and press Enter, 'help' for options, 'quit' to exit")
        
        self.running = True
        
        while self.running:
            try:
                user_input = input("\n🎯 Enter command: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'stop', 'q']:
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                self._process_command(user_input)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(1)
        
        return True
    
    def _on_voice_command(self, text: str):
        """Handle voice command from voice handler"""
        if not text or not text.strip():
            return
        
        print(f"\n🎤 Voice command: {text}")
        self._process_command(text)
    
    def _process_command(self, text: str):
        """Process a command (voice or text)"""
        # Check for stop command first
        if self.command_parser.is_stop_command(text):
            print(self.command_parser.get_feedback_message("goodbye"))
            if self.voice_handler.is_tts_available():
                self.voice_handler.speak(self.command_parser.get_feedback_message("goodbye"))
            self.running = False
            return
        
        # Parse the command
        action_data = self.command_parser.parse_command(text)
        
        if not action_data:
            error_msg = self.command_parser.get_feedback_message("error_recognizing")
            print(f"❌ {error_msg}")
            if self.voice_handler.is_tts_available():
                self.voice_handler.speak(error_msg)
            return
        
        # Show recognized command
        cmd_msg = self.command_parser.get_feedback_message("command_recognized", command=text)
        print(f"✅ {cmd_msg}")
        
        # Execute the action
        success = self.mouse_controller.execute_action(action_data)
        
        if success:
            action_msg = self.command_parser.get_feedback_message("action_executed", action=action_data["action"])
            print(f"🖱️  {action_msg}")
            if self.voice_handler.is_tts_available():
                self.voice_handler.speak(f"Action executed: {action_data['action']}")
        else:
            error_msg = self.command_parser.get_feedback_message("error_executing", error="Action failed")
            print(f"❌ {error_msg}")
            if self.voice_handler.is_tts_available():
                self.voice_handler.speak("Action failed")
    
    def _show_help(self):
        """Show help information"""
        print("\n" + "=" * 50)
        print("📖 JarvisMouseControl Help")
        print("=" * 50)
        print("🎯 Voice Commands:")
        print(self.command_parser.get_help_text())
        print("\n⌨️  Text Commands:")
        print("  help          - Show this help")
        print("  quit/exit     - Exit the program")
        print("\n🌍 Languages:")
        print("  en - English")
        print("  ur - Urdu (اردو)")
        print("  hi - Hindi (हिंदी)")
        print("=" * 50)
    
    def stop(self):
        """Stop the JarvisMouseControl agent"""
        if self.running:
            self.running = False
            
            if hasattr(self, 'voice_handler'):
                self.voice_handler.stop_listening()
            
            print("\n👋 JarvisMouseControl stopped. Goodbye!")

def main():
    """Main entry point for working JarvisMouseControl"""
    import argparse
    
    parser = argparse.ArgumentParser(description="JarvisMouseControl - Working Version")
    parser.add_argument("--language", "-l", choices=["en", "ur", "hi"], default="en", 
                       help="Language for voice commands")
    
    args = parser.parse_args()
    
    try:
        agent = WorkingJarvisMouseControl(args.language)
        agent.start()
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
    finally:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
