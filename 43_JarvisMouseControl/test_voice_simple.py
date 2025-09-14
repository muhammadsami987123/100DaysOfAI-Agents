#!/usr/bin/env python3
"""
Simple Voice Test for JarvisMouseControl
Tests voice recognition without the full application
"""

import sys
import speech_recognition as sr
import pyttsx3

def test_voice_recognition():
    """Test voice recognition with a simple command"""
    print("🎤 Testing voice recognition...")
    print("💡 Say 'hello' or 'test' when prompted...")
    
    try:
        recognizer = sr.Recognizer()
        
        # Try to find a working microphone
        mic_list = sr.Microphone.list_microphone_names()
        working_mic = None
        
        for i, mic_name in enumerate(mic_list):
            try:
                # Skip output devices
                if any(keyword in mic_name.lower() for keyword in ['output', 'speaker', 'playback']):
                    continue
                
                with sr.Microphone(device_index=i) as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    working_mic = i
                    print(f"✅ Using microphone {i}: {mic_name}")
                    break
            except:
                continue
        
        if working_mic is None:
            print("❌ No working microphone found")
            return False
        
        # Test voice recognition
        with sr.Microphone(device_index=working_mic) as source:
            print("🎤 Listening... (speak now)")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            
            print("🔄 Processing...")
            text = recognizer.recognize_google(audio, language="en-US")
            print(f"✅ Recognized: '{text}'")
            return True
            
    except sr.WaitTimeoutError:
        print("⏰ No speech detected within timeout")
        return False
    except sr.UnknownValueError:
        print("❓ Could not understand audio")
        return False
    except Exception as e:
        print(f"❌ Voice recognition error: {e}")
        return False

def test_text_to_speech():
    """Test text-to-speech"""
    print("\n🔊 Testing text-to-speech...")
    
    try:
        engine = pyttsx3.init()
        engine.say("Hello! This is a test of the text to speech system.")
        engine.runAndWait()
        print("✅ Text-to-speech working")
        return True
    except Exception as e:
        print(f"❌ Text-to-speech error: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 JarvisMouseControl - Simple Voice Test")
    print("=" * 60)
    
    # Test TTS first
    tts_ok = test_text_to_speech()
    
    # Test voice recognition
    voice_ok = test_voice_recognition()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"   Text-to-Speech: {'✅ Working' if tts_ok else '❌ Failed'}")
    print(f"   Voice Recognition: {'✅ Working' if voice_ok else '❌ Failed'}")
    print("=" * 60)
    
    if voice_ok and tts_ok:
        print("🎉 All voice features are working!")
        print("   You can now use the full application with voice control")
    elif tts_ok:
        print("⚠️  Voice recognition not working, but TTS is OK")
        print("   You can use the application in text-only mode")
    else:
        print("❌ Voice features not working")
        print("   Try running as administrator or check microphone permissions")
    
    return 0 if (voice_ok or tts_ok) else 1

if __name__ == "__main__":
    sys.exit(main())
