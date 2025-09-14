#!/usr/bin/env python3
"""
Test script to verify the microphone fix
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from main import JarvisMouseControl

def test_voice_fix():
    """Test the voice fix"""
    print("🧪 Testing voice fix...")
    
    # Create agent
    agent = JarvisMouseControl(language="en", voice_enabled=True, tts_enabled=True)
    
    # Test microphone detection
    print("\n1. Testing microphone detection...")
    working_mic = agent.find_working_microphone()
    if working_mic is not None:
        print(f"✅ Found working microphone: {working_mic}")
    else:
        print("❌ No working microphone found")
        return False
    
    # Test voice listening start
    print("\n2. Testing voice listening start...")
    if agent._start_voice_listening():
        print("✅ Voice listening started successfully")
        
        # Wait a moment
        import time
        time.sleep(2)
        
        # Stop listening
        agent.voice_handler.stop_listening()
        print("✅ Voice listening stopped successfully")
        return True
    else:
        print("❌ Failed to start voice listening")
        return False

if __name__ == "__main__":
    success = test_voice_fix()
    if success:
        print("\n🎉 Voice fix test passed!")
    else:
        print("\n❌ Voice fix test failed!")
