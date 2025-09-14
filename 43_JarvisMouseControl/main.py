#!/usr/bin/env python3
"""
🤖 JarvisMouseControl - Day 43 of #100DaysOfAI-Agents

A voice-controlled mouse automation agent with local language support (Urdu, Hindi, English).
Helps people with limited mobility, visual focus, or multitasking needs to control their 
computer mouse using voice commands.

Features:
- Voice command detection in English, Urdu, and Hindi
- Natural language understanding with OpenAI integration
- Mouse control: move, click, double click, scroll, drag & drop
- Safety features and bounds checking
- Real-time feedback and command recognition
- CLI interface with language selection

Author: Muhammad Sami Asghar Mughal
"""

import argparse
import sys
import signal
import time
import speech_recognition as sr
from pathlib import Path
from typing import Optional

from config import CONFIG, get_api_key, setup_instructions
from voice_handler import VoiceHandler
from mouse_controller import MouseController
from utils.command_parser import CommandParser

class JarvisMouseControl:
    """Main JarvisMouseControl agent class"""
    
    def __init__(self, language: str = "en", voice_enabled: bool = True, tts_enabled: bool = True):
        """Initialize JarvisMouseControl agent"""
        self.language = language
        self.running = False
        self.voice_enabled = voice_enabled
        self.tts_enabled = tts_enabled
        
        # Initialize components
        self.command_parser = CommandParser(language)
        self.mouse_controller = MouseController()
        self.voice_handler = VoiceHandler(language)
        
        # Override config settings
        CONFIG.VOICE_ENABLED = voice_enabled
        CONFIG.TTS_ENABLED = tts_enabled
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\n🛑 Shutdown signal received...")
        self.stop()
        sys.exit(0)
    
    def find_working_microphone(self):
        """Find a working microphone using the proven method from voice_working.py"""
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
        """Start the JarvisMouseControl agent"""
        print("=" * 60)
        print("🤖 JarvisMouseControl - Voice-Controlled Mouse Agent")
        print("=" * 60)
        print(f"🌍 Language: {CONFIG.LANGUAGE_NAMES.get(self.language, self.language)}")
        print(f"🎤 Voice Input: {'Enabled' if self.voice_enabled else 'Disabled'}")
        print(f"🔊 Voice Output: {'Enabled' if self.tts_enabled else 'Disabled'}")
        print(f"🖥️  Screen: {self.mouse_controller.get_screen_size()[0]}x{self.mouse_controller.get_screen_size()[1]}")
        print("=" * 60)
        
        # Show mode information
        if not self.voice_enabled and not self.tts_enabled:
            print("📝 Running in TEXT-ONLY mode")
            print("💡 Type commands and press Enter to execute them")
        elif not self.voice_enabled:
            print("📝 Running in TEXT INPUT mode with voice feedback")
            print("💡 Type commands and press Enter to execute them")
        else:
            print("🎤 Running in VOICE mode")
            print("💡 Speak commands or type them and press Enter")
        
        # Test components
        if not self._test_components():
            return False
        
        # Show welcome message
        welcome_msg = self.command_parser.get_feedback_message("welcome")
        print(f"\n{welcome_msg}")
        
        if self.tts_enabled:
            self.voice_handler.speak(welcome_msg)
        
        # Start voice listening if enabled
        if self.voice_enabled:
            # Try to start voice listening with working microphone detection
            if not self._start_voice_listening():
                print("⚠️  Voice listening failed. Switching to text-only mode.")
                self.voice_enabled = False
                CONFIG.VOICE_ENABLED = False
        
        self.running = True
        
        # Main loop
        try:
            self._main_loop()
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
        finally:
            self.stop()
        
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
        
        # Test voice handler if enabled
        if self.voice_enabled:
            try:
                # Use the improved microphone detection
                working_mic = self.find_working_microphone()
                if working_mic is None:
                    print("⚠️  Microphone not available. Switching to text-only mode.")
                    self.voice_enabled = False
                    CONFIG.VOICE_ENABLED = False
                else:
                    print("✅ Microphone: OK")
            except Exception as e:
                print(f"⚠️  Microphone test failed: {e}")
                print("⚠️  Switching to text-only mode.")
                self.voice_enabled = False
                CONFIG.VOICE_ENABLED = False
        
        if self.tts_enabled:
            try:
                if not self.voice_handler.test_speakers():
                    print("⚠️  Speakers not available. Disabling voice feedback.")
                    self.tts_enabled = False
                    CONFIG.TTS_ENABLED = False
                else:
                    print("✅ Speakers: OK")
            except Exception as e:
                print(f"⚠️  Speaker test failed: {e}")
                print("⚠️  Disabling voice feedback.")
                self.tts_enabled = False
                CONFIG.TTS_ENABLED = False
        
        print("✅ All components tested successfully!")
        return True
    
    def _main_loop(self):
        """Main application loop"""
        if self.voice_enabled:
            print("\n🎤 Continuous voice listening active!")
            print("💡 Speak commands or type 'help' for options, 'quit' to exit")
        else:
            print("\n📝 Text input mode")
            print("💡 Type commands and press Enter, 'help' for options, 'quit' to exit")
        
        while self.running:
            try:
                if not self.voice_enabled:
                    # Text input mode
                    user_input = input("\n🎯 Enter command: ").strip()
                    
                    if not user_input:
                        continue
                    
                    if user_input.lower() in ['quit', 'exit', 'stop', 'q']:
                        break
                    
                    if user_input.lower() == 'help':
                        self._show_help()
                        continue
                    
                    if user_input.lower().startswith('lang '):
                        new_lang = user_input.split()[1] if len(user_input.split()) > 1 else None
                        if new_lang and self._change_language(new_lang):
                            continue
                        else:
                            print("❌ Invalid language. Use: en, ur, hi")
                            continue
                    
                    if user_input.lower() == 'voice':
                        # Try to enable voice mode
                        if self._enable_voice_mode():
                            continue
                        else:
                            print("❌ Could not enable voice mode")
                            continue
                    
                    self._process_command(user_input)
                
                else:
                    # Voice mode - just wait for voice commands
                    time.sleep(0.1)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(1)
    
    def _enable_voice_mode(self) -> bool:
        """Try to enable voice mode"""
        print("🎤 Attempting to enable voice mode...")
        
        # Test microphone
        working_mic = self.find_working_microphone()
        if working_mic is None:
            print("❌ No working microphone found")
            return False
        
        # Start voice listening
        if self.voice_handler.start_listening(self._on_voice_command, working_mic):
            self.voice_enabled = True
            CONFIG.VOICE_ENABLED = True
            print("✅ Voice mode enabled!")
            return True
        else:
            print("❌ Failed to start voice listening")
            return False
    
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
            if self.tts_enabled:
                self.voice_handler.speak(self.command_parser.get_feedback_message("goodbye"))
            self.running = False
            return
        
        # Parse the command
        action_data = self.command_parser.parse_command(text)
        
        if not action_data:
            error_msg = self.command_parser.get_feedback_message("error_recognizing")
            print(f"❌ {error_msg}")
            if self.tts_enabled:
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
            if self.tts_enabled:
                self.voice_handler.speak(f"Action executed: {action_data['action']}")
        else:
            error_msg = self.command_parser.get_feedback_message("error_executing", error="Action failed")
            print(f"❌ {error_msg}")
            if self.tts_enabled:
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
        print("  lang <code>   - Change language (en/ur/hi)")
        print("  voice         - Try to enable voice mode")
        print("  quit/exit     - Exit the program")
        print("\n🌍 Languages:")
        print("  en - English")
        print("  ur - Urdu (اردو)")
        print("  hi - Hindi (हिंदी)")
        print("=" * 50)
    
    def _change_language(self, language: str) -> bool:
        """Change the agent language"""
        if language not in CONFIG.SUPPORTED_LANGUAGES:
            return False
        
        self.language = language
        self.command_parser.set_language(language)
        self.voice_handler.set_language(language)
        
        lang_msg = self.command_parser.get_feedback_message("language_changed", language=CONFIG.LANGUAGE_NAMES.get(language, language))
        print(f"🌍 {lang_msg}")
        
        if self.tts_enabled:
            self.voice_handler.speak(lang_msg)
        
        return True
    
    def stop(self):
        """Stop the JarvisMouseControl agent"""
        if self.running:
            self.running = False
            
            if self.voice_enabled:
                self.voice_handler.stop_listening()
            
            print("\n👋 JarvisMouseControl stopped. Goodbye!")

def main():
    """Main entry point for JarvisMouseControl"""
    parser = argparse.ArgumentParser(
        description="JarvisMouseControl - Voice-controlled mouse automation agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --language en                    # English mode (default)
  python main.py --language ur                    # Urdu mode
  python main.py --language hi                    # Hindi mode
  python main.py --no-voice                       # Text input only
  python main.py --no-tts                         # No voice feedback
  python main.py --test                           # Test components only
  python voice_working.py                         # Working voice demo
        """
    )
    
    # Language selection
    parser.add_argument(
        "--language", "-l",
        type=str,
        choices=["en", "ur", "hi"],
        default="en",
        help="Language for voice commands (default: en)"
    )
    
    # Voice settings
    parser.add_argument(
        "--no-voice",
        action="store_true",
        help="Disable voice input (text mode only)"
    )
    
    parser.add_argument(
        "--no-tts",
        action="store_true",
        help="Disable text-to-speech feedback"
    )
    
    # Test mode
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test components and exit"
    )
    
    # Debug mode
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output"
    )
    
    args = parser.parse_args()
    
    # Check API key for OpenAI features
    api_key = get_api_key()
    if not api_key:
        print("⚠️  OpenAI API key not found!")
        print("   Some advanced features may not work without it.")
        print("   Run with --help for setup instructions.")
        print()
    
    # Create and configure agent
    agent = JarvisMouseControl(
        language=args.language,
        voice_enabled=not args.no_voice,
        tts_enabled=not args.no_tts
    )
    
    # Test mode
    if args.test:
        print("🧪 Testing JarvisMouseControl components...")
        if agent._test_components():
            print("✅ All tests passed!")
            return 0
        else:
            print("❌ Some tests failed!")
            return 1
    
    # Start the agent
    try:
        success = agent.start()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
