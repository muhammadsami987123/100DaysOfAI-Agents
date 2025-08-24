"""
Main application for MoodMusicAgent - Emotion-Based Music Player
"""
import os
import sys
import time
from typing import Optional, Dict, Any
from config import Config
from mood_detector import MoodDetector
from music_service import MusicService
from mood_history import MoodHistory
from voice_interface import VoiceInterface

class MoodMusicAgent:
    """Main MoodMusicAgent application"""
    
    def __init__(self):
        self.mood_detector = MoodDetector()
        self.music_service = MusicService()
        self.mood_history = MoodHistory()
        self.voice_interface = VoiceInterface()
        
        # Application state
        self.current_mood = None
        self.current_music = None
        self.is_running = True
        
        # Validate configuration
        self._validate_setup()
    
    def _validate_setup(self):
        """Validate the application setup"""
        print("🔍 Validating MoodMusicAgent setup...")
        
        # Check configuration
        config_issues = Config.validate_config()
        if config_issues:
            print("⚠️  Configuration issues found:")
            for issue in config_issues:
                print(f"   - {issue}")
        else:
            print("✅ Configuration validated")
        
        # Check music sources
        available_sources = self.music_service.get_available_sources()
        if available_sources:
            print(f"✅ Available music sources: {', '.join(available_sources)}")
        else:
            print("❌ No music sources available")
        
        # Check voice interface
        voice_status = self.voice_interface.get_voice_status()
        if voice_status["voice_input_enabled"] or voice_status["voice_output_enabled"]:
            print("✅ Voice interface available")
        else:
            print("⚠️  Voice interface not available")
        
        print()
    
    def run(self):
        """Main application loop"""
        self._show_welcome()
        
        while self.is_running:
            try:
                self._show_main_menu()
                choice = self._get_user_choice()
                self._handle_main_menu_choice(choice)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using MoodMusicAgent!")
                self.cleanup()
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                continue
    
    def _show_welcome(self):
        """Display welcome message"""
        print("🎵" * 50)
        print("🎵 Welcome to MoodMusicAgent - Your Emotion-Based Music Player! 🎵")
        print("🎵" * 50)
        print()
        
        if self.voice_interface.enable_voice_output:
            self.voice_interface.speak_instructions()
    
    def _show_main_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("🎵 MoodMusicAgent Main Menu")
        print("="*60)
        print("1. 🎭 Tell me your mood")
        print("2. 🎤 Voice mood detection")
        print("3. 📊 View mood history")
        print("4. 🎧 Music controls")
        print("5. ⚙️  Settings")
        print("6. 🧪 Test features")
        print("7. ❓ Help")
        print("8. 🚪 Exit")
        print("="*60)
    
    def _get_user_choice(self) -> str:
        """Get user choice from main menu"""
        while True:
            choice = input("\nEnter your choice (1-8): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                return choice
            print("❌ Please enter a number between 1 and 8")
    
    def _handle_main_menu_choice(self, choice: str):
        """Handle main menu choice"""
        if choice == '1':
            self._text_mood_detection()
        elif choice == '2':
            self._voice_mood_detection()
        elif choice == '3':
            self._show_mood_history()
        elif choice == '4':
            self._show_music_controls()
        elif choice == '5':
            self._show_settings()
        elif choice == '6':
            self._test_features()
        elif choice == '7':
            self._show_help()
        elif choice == '8':
            self._exit_application()
    
    def _text_mood_detection(self):
        """Handle text-based mood detection"""
        print("\n🎭 Text Mood Detection")
        print("-" * 30)
        
        # Show mood suggestions
        mood_suggestions = self.mood_detector.get_mood_suggestions()
        print("Available moods:")
        for i, mood in enumerate(mood_suggestions, 1):
            mood_config = Config.get_mood_config(mood)
            print(f"   {i}. {mood.title()} - {mood_config['description']}")
        
        print("\nYou can:")
        print("1. Type a mood number (1-8)")
        print("2. Type your mood in words (e.g., 'I'm feeling happy')")
        print("3. Type 'back' to return to main menu")
        
        while True:
            user_input = input("\nHow are you feeling? ").strip().lower()
            
            if user_input == 'back':
                return
            
            # Check if it's a number
            try:
                mood_index = int(user_input) - 1
                if 0 <= mood_index < len(mood_suggestions):
                    selected_mood = mood_suggestions[mood_index]
                    self._process_mood(selected_mood, 0.9, "manual_selection")
                    break
                else:
                    print("❌ Invalid mood number")
                    continue
            except ValueError:
                # Treat as text input
                pass
            
            # Process text input
            if user_input:
                self._process_text_mood(user_input)
                break
    
    def _voice_mood_detection(self):
        """Handle voice-based mood detection"""
        print("\n🎤 Voice Mood Detection")
        print("-" * 30)
        
        if not self.voice_interface.enable_voice_input:
            print("❌ Voice input not available")
            return
        
        print("I'll listen for your mood. Please speak clearly.")
        print("Say something like 'I'm feeling happy' or 'I'm sad today'")
        
        voice_result = self.voice_interface.listen_for_mood(timeout=15)
        
        if voice_result:
            text = voice_result["text"]
            print(f"\n🎯 Detected text: \"{text}\"")
            self._process_text_mood(text)
        else:
            print("❌ Could not detect mood from voice")
    
    def _process_text_mood(self, text: str):
        """Process text input for mood detection"""
        print(f"\n🔍 Analyzing your mood: \"{text}\"")
        
        # Detect mood
        mood_result = self.mood_detector.detect_mood(text)
        
        if mood_result and mood_result["confidence"] > 0.3:
            mood = mood_result["mood"]
            confidence = mood_result["confidence"]
            method = mood_result["method"]
            
            print(f"😊 Mood detected: {mood.title()}")
            print(f"📊 Confidence: {confidence:.1%}")
            print(f"🔍 Method: {method}")
            
            # Speak mood detection if voice output is enabled
            if self.voice_interface.enable_voice_output:
                self.voice_interface.speak_mood_detection(mood, confidence)
            
            # Process the mood
            self._process_mood(mood, confidence, method, text)
            
        else:
            print("❓ Could not determine your mood from the text")
            print("Try being more specific about how you're feeling")
    
    def _process_mood(self, mood: str, confidence: float, method: str, user_input: str = ""):
        """Process detected mood and find music"""
        self.current_mood = mood
        
        print(f"\n🔍 Finding music for your {mood} mood...")
        
        # Get music recommendation
        music_data = self.music_service.get_music_for_mood(mood)
        
        if music_data:
            self.current_music = music_data
            
            # Add to mood history
            self.mood_history.add_mood_entry(
                mood=mood,
                confidence=confidence,
                method=method,
                music_played=music_data,
                user_input=user_input
            )
            
            # Play the music
            if self.music_service.play_music(music_data):
                print("✅ Music started successfully!")
                
                # Speak music selection if voice output is enabled
                if self.voice_interface.enable_voice_output:
                    self.voice_interface.speak_music_selection(music_data)
                
                # Show music controls
                self._show_music_controls()
            else:
                print("❌ Failed to start music playback")
        else:
            print("❌ Could not find suitable music for your mood")
    
    def _show_mood_history(self):
        """Display mood history and analytics"""
        print("\n📊 Mood History & Analytics")
        print("-" * 30)
        
        # Get summary stats
        summary = self.mood_history.get_stats_summary()
        
        if "message" in summary:
            print(summary["message"])
            return
        
        print(f"📈 Total mood entries: {summary['total_entries']}")
        print(f"🎭 Unique moods: {', '.join(summary['unique_moods'])}")
        print(f"📅 Date range: {summary['date_range']['start']} to {summary['date_range']['end']}")
        print(f"🎯 Most recent mood: {summary['most_recent_mood']}")
        print(f"📊 Average confidence: {summary['average_confidence']:.1%}")
        
        # Show recent trends
        print("\n📊 Recent Trends (Last 7 days):")
        trends = self.mood_history.get_mood_trends(days=7)
        
        if "message" not in trends:
            print(f"   Most common mood: {trends['most_common_mood']}")
            print(f"   Mood distribution: {trends['mood_distribution']}")
        
        # Show correlations
        print("\n🔗 Mood Correlations:")
        correlations = self.mood_history.get_mood_correlations()
        
        if "message" not in correlations:
            print(f"   Morning mood: {correlations['time_correlations']['morning']}")
            print(f"   Evening mood: {correlations['time_correlations']['evening']}")
            print(f"   Weekday mood: {correlations['day_correlations']['weekday']}")
            print(f"   Weekend mood: {correlations['day_correlations']['weekend']}")
        
        input("\nPress Enter to continue...")
    
    def _show_music_controls(self):
        """Show music playback controls"""
        if not self.current_music:
            print("\n❌ No music currently playing")
            return
        
        print(f"\n🎧 Music Controls - {self.current_music['title']}")
        print("-" * 40)
        print("1. ⏸️  Pause")
        print("2. ▶️  Resume")
        print("3. ⏹️  Stop")
        print("4. 🔊 Volume control")
        print("5. 🔄 Next track")
        print("6. ⬅️  Back to main menu")
        
        while True:
            choice = input("\nEnter choice (1-6): ").strip()
            
            if choice == '1':
                self.music_service.pause_music()
            elif choice == '2':
                self.music_service.resume_music()
            elif choice == '3':
                self.music_service.stop_music()
                self.current_music = None
                break
            elif choice == '4':
                self._volume_control()
            elif choice == '5':
                # For now, just restart the same track
                if self.current_mood:
                    self._process_mood(self.current_mood, 0.8, "manual")
                break
            elif choice == '6':
                break
            else:
                print("❌ Invalid choice")
    
    def _volume_control(self):
        """Handle volume control"""
        print("\n🔊 Volume Control")
        print("-" * 20)
        
        current_volume = self.music_service.volume
        print(f"Current volume: {int(current_volume * 100)}%")
        
        while True:
            try:
                new_volume = input("Enter new volume (0-100) or 'back': ").strip()
                
                if new_volume.lower() == 'back':
                    break
                
                volume_int = int(new_volume)
                if 0 <= volume_int <= 100:
                    volume_float = volume_int / 100.0
                    if self.music_service.set_volume(volume_float):
                        if self.voice_interface.enable_voice_output:
                            self.voice_interface.speak_volume_change(volume_float)
                        break
                else:
                    print("❌ Volume must be between 0 and 100")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def _show_settings(self):
        """Show settings menu"""
        print("\n⚙️  Settings")
        print("-" * 20)
        print("1. 🎵 Music source preferences")
        print("2. 🎤 Voice settings")
        print("3. 📊 Mood history settings")
        print("4. ⬅️  Back to main menu")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            self._music_source_settings()
        elif choice == '2':
            self._voice_settings()
        elif choice == '3':
            self._mood_history_settings()
    
    def _music_source_settings(self):
        """Configure music source preferences"""
        print("\n🎵 Music Source Settings")
        print("-" * 30)
        
        status = self.music_service.get_source_status()
        available = self.music_service.get_available_sources()
        
        print("Available sources:")
        for source in ["spotify", "youtube", "local"]:
            status_icon = "✅" if status.get(source, False) else "❌"
            print(f"   {status_icon} {source.title()}")
        
        if available:
            print(f"\nCurrently using: {', '.join(available)}")
        else:
            print("\n❌ No music sources available")
        
        input("\nPress Enter to continue...")
    
    def _voice_settings(self):
        """Configure voice interface settings"""
        print("\n🎤 Voice Settings")
        print("-" * 20)
        
        status = self.voice_interface.get_voice_status()
        print(f"Voice input: {'✅ Enabled' if status['voice_input_enabled'] else '❌ Disabled'}")
        print(f"Voice output: {'✅ Enabled' if status['voice_output_enabled'] else '❌ Disabled'}")
        
        if status['text_to_speech_available']:
            voices = self.voice_interface.get_available_voices()
            if voices:
                print(f"\nAvailable voices: {len(voices)}")
                for voice in voices[:3]:  # Show first 3
                    print(f"   - {voice['name']} ({voice['languages'][0]})")
        
        input("\nPress Enter to continue...")
    
    def _mood_history_settings(self):
        """Configure mood history settings"""
        print("\n📊 Mood History Settings")
        print("-" * 30)
        
        summary = self.mood_history.get_stats_summary()
        if "message" not in summary:
            print(f"Total entries: {summary['total_entries']}")
            print(f"Date range: {summary['date_range']['days']} days")
        
        print("\nOptions:")
        print("1. Export history (JSON)")
        print("2. Export history (CSV)")
        print("3. Clear history")
        print("4. Back")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            export_data = self.mood_history.export_history("json")
            filename = f"mood_history_{int(time.time())}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(export_data)
            print(f"✅ History exported to {filename}")
        
        elif choice == '2':
            export_data = self.mood_history.export_history("csv")
            filename = f"mood_history_{int(time.time())}.csv"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(export_data)
            print(f"✅ History exported to {filename}")
        
        elif choice == '3':
            confirm = input("⚠️  Are you sure you want to clear all mood history? (yes/no): ").strip().lower()
            if confirm == 'yes':
                if self.mood_history.clear_history():
                    print("✅ Mood history cleared")
                else:
                    print("❌ Failed to clear mood history")
    
    def _test_features(self):
        """Test various features"""
        print("\n🧪 Feature Testing")
        print("-" * 20)
        print("1. 🎤 Test voice interface")
        print("2. 🎵 Test music sources")
        print("3. 🧠 Test mood detection")
        print("4. ⬅️  Back to main menu")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            self._test_voice_interface()
        elif choice == '2':
            self._test_music_sources()
        elif choice == '3':
            self._test_mood_detection()
    
    def _test_voice_interface(self):
        """Test voice interface functionality"""
        print("\n🎤 Testing Voice Interface")
        print("-" * 30)
        
        results = self.voice_interface.test_voice_interface()
        
        print("Test Results:")
        print(f"   Speech Recognition: {'✅' if results['speech_recognition'] else '❌'}")
        print(f"   Text-to-Speech: {'✅' if results['text_to_speech'] else '❌'}")
        print(f"   Microphone: {'✅' if results['microphone'] else '❌'}")
        print(f"   Overall: {'✅' if results['overall'] else '❌'}")
        
        input("\nPress Enter to continue...")
    
    def _test_music_sources(self):
        """Test music sources"""
        print("\n🎵 Testing Music Sources")
        print("-" * 30)
        
        available_sources = self.music_service.get_available_sources()
        
        for source in available_sources:
            print(f"\nTesting {source.title()}...")
            try:
                # Test with a simple mood
                test_music = self.music_service.get_music_for_mood("happy", source)
                if test_music:
                    print(f"   ✅ {source.title()} working")
                else:
                    print(f"   ❌ {source.title()} no results")
            except Exception as e:
                print(f"   ❌ {source.title()} error: {e}")
        
        input("\nPress Enter to continue...")
    
    def _test_mood_detection(self):
        """Test mood detection"""
        print("\n🧠 Testing Mood Detection")
        print("-" * 30)
        
        test_texts = [
            "I'm feeling really happy today!",
            "I'm so sad and depressed",
            "I need to focus on my work",
            "I'm feeling romantic and loving",
            "I'm stressed about my deadline"
        ]
        
        for text in test_texts:
            print(f"\nTesting: \"{text}\"")
            result = self.mood_detector.detect_mood(text)
            if result:
                print(f"   Detected: {result['mood']} (confidence: {result['confidence']:.1%})")
            else:
                print("   ❌ No mood detected")
        
        input("\nPress Enter to continue...")
    
    def _show_help(self):
        """Show help information"""
        print("\n❓ Help & Information")
        print("-" * 30)
        print("🎵 MoodMusicAgent helps you find the perfect music for your mood!")
        print("\nHow to use:")
        print("1. Tell me how you're feeling (text or voice)")
        print("2. I'll analyze your mood and find suitable music")
        print("3. Control playback with the music controls")
        print("4. Track your mood patterns over time")
        
        print("\nAvailable moods:")
        for mood, config in Config.MOOD_CATEGORIES.items():
            print(f"   • {mood.title()}: {config['description']}")
        
        print("\nMusic sources:")
        sources = self.music_service.get_available_sources()
        for source in sources:
            print(f"   • {source.title()}")
        
        print("\nVoice commands:")
        print("   • Say 'I'm feeling [mood]' for voice mood detection")
        print("   • Voice output will announce mood detection and music selection")
        
        input("\nPress Enter to continue...")
    
    def _exit_application(self):
        """Exit the application"""
        print("\n👋 Thanks for using MoodMusicAgent!")
        print("Hope the music helped improve your mood! 🎵")
        self.cleanup()
        self.is_running = False
    
    def cleanup(self):
        """Clean up resources"""
        try:
            # Stop music
            if self.music_service.is_playing:
                self.music_service.stop_music()
            
            # Clean up voice interface
            self.voice_interface.cleanup()
            
        except Exception as e:
            print(f"⚠️  Error during cleanup: {e}")

def main():
    """Main entry point"""
    try:
        agent = MoodMusicAgent()
        agent.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
