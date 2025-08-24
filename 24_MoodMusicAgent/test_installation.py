"""
Test script for MoodMusicAgent - verifies installation and basic functionality
"""
import sys
import os
from pathlib import Path

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("   MoodMusicAgent requires Python 3.8+")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def test_dependencies():
    """Test required dependencies"""
    print("\n📦 Testing dependencies...")
    
    required_packages = [
        "pygame",
        "textblob", 
        "nltk",
        "requests",
        "dotenv"
    ]
    
    optional_packages = [
        "speech_recognition",
        "pyttsx3",
        "spotipy",
        "youtube_search_python"
    ]
    
    all_good = True
    
    # Test required packages
    print("Required packages:")
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NOT INSTALLED")
            all_good = False
    
    # Test optional packages
    print("\nOptional packages:")
    for package in optional_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ⚠️  {package} - Not installed (optional)")
    
    return all_good

def test_configuration():
    """Test configuration setup"""
    print("\n⚙️  Testing configuration...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
        
        # Read and check basic structure
        try:
            with open(env_file, 'r') as f:
                content = f.read()
                if "SPOTIFY_CLIENT_ID" in content or "YOUTUBE_API_KEY" in content:
                    print("✅ Environment variables configured")
                else:
                    print("⚠️  No API keys found in .env (optional)")
        except Exception as e:
            print(f"❌ Error reading .env file: {e}")
    else:
        print("⚠️  .env file not found - copying from template...")
        try:
            import shutil
            shutil.copy("env.example", ".env")
            print("✅ .env file created from template")
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
    
    # Check directories
    directories = ["data", "logs"]
    for directory in directories:
        dir_path = Path(directory)
        if dir_path.exists():
            print(f"✅ {directory}/ directory exists")
        else:
            print(f"⚠️  {directory}/ directory missing - creating...")
            try:
                dir_path.mkdir(exist_ok=True)
                print(f"✅ {directory}/ directory created")
            except Exception as e:
                print(f"❌ Error creating {directory}/ directory: {e}")
    
    return True

def test_mood_detection():
    """Test mood detection functionality"""
    print("\n🧠 Testing mood detection...")
    
    try:
        from config import Config
        from mood_detector import MoodDetector
        
        # Test configuration
        mood_categories = Config.MOOD_CATEGORIES
        print(f"✅ Loaded {len(mood_categories)} mood categories")
        
        # Test mood detector
        detector = MoodDetector()
        print("✅ Mood detector initialized")
        
        # Test mood detection
        test_text = "I'm feeling really happy today!"
        result = detector.detect_mood(test_text)
        
        if result and "mood" in result:
            print(f"✅ Mood detection working - detected: {result['mood']}")
            return True
        else:
            print("❌ Mood detection failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing mood detection: {e}")
        return False

def test_music_service():
    """Test music service functionality"""
    print("\n🎵 Testing music service...")
    
    try:
        from music_service import MusicService
        
        service = MusicService()
        available_sources = service.get_available_sources()
        
        if available_sources:
            print(f"✅ Music service initialized with sources: {', '.join(available_sources)}")
            return True
        else:
            print("⚠️  Music service initialized but no sources available")
            return True
            
    except Exception as e:
        print(f"❌ Error testing music service: {e}")
        return False

def test_voice_interface():
    """Test voice interface functionality"""
    print("\n🎤 Testing voice interface...")
    
    try:
        from voice_interface import VoiceInterface
        
        voice = VoiceInterface()
        status = voice.get_voice_status()
        
        print(f"   Voice input: {'✅' if status['voice_input_enabled'] else '❌'}")
        print(f"   Voice output: {'✅' if status['voice_output_enabled'] else '❌'}")
        
        if status['voice_input_enabled'] or status['voice_output_enabled']:
            print("✅ Voice interface working")
            return True
        else:
            print("⚠️  Voice interface not available (optional)")
            return True
            
    except Exception as e:
        print(f"❌ Error testing voice interface: {e}")
        return False

def test_mood_history():
    """Test mood history functionality"""
    print("\n📊 Testing mood history...")
    
    try:
        from mood_history import MoodHistory
        
        history = MoodHistory()
        summary = history.get_stats_summary()
        
        if "message" in summary:
            print("✅ Mood history initialized (no data yet)")
        else:
            print(f"✅ Mood history working - {summary['total_entries']} entries")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing mood history: {e}")
        return False

def run_all_tests():
    """Run all installation tests"""
    print("🧪 MoodMusicAgent Installation Test")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Configuration", test_configuration),
        ("Mood Detection", test_mood_detection),
        ("Music Service", test_music_service),
        ("Voice Interface", test_voice_interface),
        ("Mood History", test_mood_history)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! MoodMusicAgent is ready to use.")
        print("\nTo start the agent:")
        print("   python main.py")
        print("\nTo run the demo:")
        print("   python demo.py")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        print("Please check the errors above and fix any issues.")
        print("\nCommon solutions:")
        print("1. Run: pip install -r requirements.txt")
        print("2. Check your Python version (3.8+ required)")
        print("3. Verify your .env file configuration")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Testing interrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Testing failed with error: {e}")
        sys.exit(1)
