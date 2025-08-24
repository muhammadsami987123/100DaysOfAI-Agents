"""
Demo script for MoodMusicAgent - showcases capabilities without full setup
"""
import sys
import time
from config import Config

def demo_mood_detection():
    """Demo mood detection capabilities"""
    print("🧠 Mood Detection Demo")
    print("=" * 40)
    
    # Show available moods
    print("\nAvailable mood categories:")
    for mood, config in Config.MOOD_CATEGORIES.items():
        print(f"   🎭 {mood.title()}: {config['description']}")
        print(f"      Energy: {config['energy_level']}, Tempo: {config['tempo']}")
        print(f"      Volume: {config['volume_multiplier']:.1f}x")
    
    # Demo mood detection
    print("\n🎯 Mood Detection Examples:")
    test_texts = [
        "I'm feeling really happy today!",
        "I'm so sad and depressed about everything",
        "I need to focus on my work and studies",
        "I'm feeling romantic and loving",
        "I'm stressed about my deadline tomorrow",
        "I'm motivated to achieve my goals",
        "I want to relax and unwind",
        "I'm feeling energetic and pumped up!"
    ]
    
    for text in test_texts:
        print(f"\nText: \"{text}\"")
        # Simulate mood detection
        if "happy" in text.lower():
            mood = "happy"
            confidence = 0.9
        elif "sad" in text.lower() or "depressed" in text.lower():
            mood = "sad"
            confidence = 0.85
        elif "focus" in text.lower() or "work" in text.lower() or "studies" in text.lower():
            mood = "focus"
            confidence = 0.8
        elif "romantic" in text.lower() or "loving" in text.lower():
            mood = "romantic"
            confidence = 0.9
        elif "stressed" in text.lower() or "deadline" in text.lower():
            mood = "stressed"
            confidence = 0.8
        elif "motivated" in text.lower() or "goals" in text.lower():
            mood = "motivated"
            confidence = 0.85
        elif "relax" in text.lower() or "unwind" in text.lower():
            mood = "relaxed"
            confidence = 0.8
        elif "energetic" in text.lower() or "pumped" in text.lower():
            mood = "energetic"
            confidence = 0.9
        else:
            mood = "neutral"
            confidence = 0.5
        
        mood_config = Config.get_mood_config(mood)
        print(f"   Detected: {mood.title()} (confidence: {confidence:.1%})")
        print(f"   Music: {mood_config['description']}")
        print(f"   Genres: {', '.join(mood_config['genres'])}")

def demo_music_mapping():
    """Demo music mapping for different moods"""
    print("\n🎵 Music Mapping Demo")
    print("=" * 40)
    
    print("\nHow moods map to music:")
    
    mood_examples = {
        "happy": {
            "example_tracks": ["Happy - Pharrell Williams", "Walking on Sunshine - Katrina & The Waves"],
            "playlist": "Upbeat Pop Mix",
            "energy": "High energy, cheerful beats"
        },
        "sad": {
            "example_tracks": ["Mad World - Gary Jules", "Hallelujah - Jeff Buckley"],
            "playlist": "Melancholic Ballads",
            "energy": "Slow, emotional, soothing"
        },
        "energetic": {
            "example_tracks": ["Eye of the Tiger - Survivor", "We Will Rock You - Queen"],
            "playlist": "High Energy Workout Mix",
            "energy": "Fast tempo, powerful, motivating"
        },
        "relaxed": {
            "example_tracks": ["Weightless - Marconi Union", "Claire de Lune - Debussy"],
            "playlist": "Chill Ambient Sounds",
            "energy": "Calm, peaceful, meditative"
        },
        "focus": {
            "example_tracks": ["Lofi Hip Hop Radio", "Classical Study Music"],
            "playlist": "Focus & Concentration",
            "energy": "Steady, non-distracting, instrumental"
        }
    }
    
    for mood, info in mood_examples.items():
        print(f"\n🎭 {mood.title()}:")
        print(f"   Playlist: {info['playlist']}")
        print(f"   Energy: {info['energy']}")
        print(f"   Examples: {', '.join(info['example_tracks'])}")

def demo_voice_interface():
    """Demo voice interface capabilities"""
    print("\n🎤 Voice Interface Demo")
    print("=" * 40)
    
    print("\nVoice Input Capabilities:")
    print("   • Listen for mood descriptions")
    print("   • Convert speech to text")
    print("   • Process natural language")
    print("   • Support multiple languages")
    
    print("\nVoice Output Capabilities:")
    print("   • Announce detected mood")
    print("   • Confirm music selection")
    print("   • Provide feedback and instructions")
    print("   • Adjustable speech rate and volume")
    
    print("\nExample Voice Commands:")
    voice_examples = [
        "I'm feeling happy today",
        "I need to focus on my work",
        "I'm feeling a bit sad",
        "I want to relax and unwind",
        "I'm motivated to exercise"
    ]
    
    for example in voice_examples:
        print(f"   • \"{example}\"")

def demo_mood_history():
    """Demo mood history and analytics"""
    print("\n📊 Mood History & Analytics Demo")
    print("=" * 40)
    
    print("\nTracking Capabilities:")
    print("   • Mood entries with timestamps")
    print("   • Confidence levels and detection methods")
    print("   • Music played for each mood")
    print("   • User input text preservation")
    
    print("\nAnalytics Features:")
    print("   • Mood trends over time")
    print("   • Time-of-day correlations")
    print("   • Day-of-week patterns")
    print("   • Music preference analysis")
    
    print("\nExport Options:")
    print("   • JSON format for data analysis")
    print("   • CSV format for spreadsheets")
    print("   • Historical data preservation")
    print("   • Privacy-focused local storage")

def demo_music_sources():
    """Demo different music sources"""
    print("\n🎵 Music Sources Demo")
    print("=" * 40)
    
    print("\nAvailable Music Sources:")
    
    sources = {
        "Local Files": {
            "description": "MP3, WAV, OGG files from your computer",
            "pros": "No internet required, instant access, no ads",
            "cons": "Limited to your music library, manual organization"
        },
        "Spotify": {
            "description": "Premium streaming service integration",
            "pros": "Huge library, curated playlists, high quality",
            "cons": "Requires premium subscription, API setup"
        },
        "YouTube": {
            "description": "Free music streaming via YouTube",
            "pros": "Free, vast selection, music videos",
            "cons": "Ads, variable quality, requires internet"
        }
    }
    
    for source, info in sources.items():
        print(f"\n📡 {source}:")
        print(f"   {info['description']}")
        print(f"   ✅ {info['pros']}")
        print(f"   ⚠️  {info['cons']}")

def run_full_demo():
    """Run the complete demo"""
    print("🎵" * 60)
    print("🎵 Welcome to MoodMusicAgent Demo! 🎵")
    print("🎵" * 60)
    print("\nThis demo showcases the capabilities of MoodMusicAgent")
    print("without requiring full setup or API keys.")
    print("\nPress Enter after each section to continue...")
    
    input("\nPress Enter to start the demo...")
    
    demo_mood_detection()
    input("\nPress Enter to continue...")
    
    demo_music_mapping()
    input("\nPress Enter to continue...")
    
    demo_voice_interface()
    input("\nPress Enter to continue...")
    
    demo_mood_history()
    input("\nPress Enter to continue...")
    
    demo_music_sources()
    
    print("\n" + "="*60)
    print("🎵 Demo Complete! 🎵")
    print("="*60)
    print("\nTo try the full MoodMusicAgent:")
    print("1. Run: install.bat (Windows) or pip install -r requirements.txt")
    print("2. Set up your .env file with API keys (optional)")
    print("3. Run: python main.py")
    print("\nFor more information, see README.md")
    print("\nHappy listening! 🎧✨")

if __name__ == "__main__":
    try:
        run_full_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for checking out MoodMusicAgent!")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("Please check your setup and try again.")
