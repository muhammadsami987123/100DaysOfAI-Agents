#!/usr/bin/env python3
"""
Microphone Permission Fix for JarvisMouseControl
Attempts to fix Windows microphone permission issues
"""

import sys
import os
import subprocess
import speech_recognition as sr

def check_admin_privileges():
    """Check if running with administrator privileges"""
    try:
        if os.name == 'nt':  # Windows
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.getuid() == 0
    except:
        return False

def fix_microphone_permissions():
    """Try to fix microphone permission issues"""
    print("🔧 Attempting to fix microphone permissions...")
    
    if not check_admin_privileges():
        print("⚠️  Not running as administrator")
        print("💡 For best results, run this script as administrator")
        print("   Right-click Command Prompt → Run as administrator")
        print("   Then run: python fix_mic_permissions.py")
        return False
    
    print("✅ Running with administrator privileges")
    
    # Try to enable microphone access
    try:
        # This is a simplified approach - in reality, Windows permissions
        # need to be changed through the Settings app
        print("💡 Please manually enable microphone permissions:")
        print("   1. Press Windows + I to open Settings")
        print("   2. Go to Privacy & Security → Microphone")
        print("   3. Turn ON 'Microphone access'")
        print("   4. Turn ON 'Let apps access your microphone'")
        print("   5. Turn ON 'Let desktop apps access your microphone'")
        print("   6. Restart the application")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_microphone_access():
    """Test microphone access with improved detection"""
    print("\n🧪 Testing microphone access...")
    
    try:
        recognizer = sr.Recognizer()
        mic_list = sr.Microphone.list_microphone_names()
        
        if not mic_list:
            print("❌ No microphones detected")
            return False
        
        print(f"🎤 Found {len(mic_list)} microphone(s)")
        
        # Test each microphone
        working_mics = []
        for i, mic_name in enumerate(mic_list):
            try:
                # Skip output devices
                if any(keyword in mic_name.lower() for keyword in ['output', 'speaker', 'playback']):
                    continue
                
                with sr.Microphone(device_index=i) as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    print(f"✅ Microphone {i}: {mic_name} - Working")
                    working_mics.append(i)
            except Exception as e:
                print(f"❌ Microphone {i}: {mic_name} - Failed")
                continue
        
        if working_mics:
            print(f"\n✅ Found {len(working_mics)} working microphone(s)")
            return True
        else:
            print("\n❌ No working microphones found")
            return False
            
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("🎤 JarvisMouseControl - Microphone Permission Fix")
    print("=" * 60)
    
    # Check admin privileges
    if not check_admin_privileges():
        print("⚠️  WARNING: Not running as administrator")
        print("   Some fixes may not work without admin privileges")
        print()
    
    # Test current microphone access
    if test_microphone_access():
        print("\n🎉 Microphone is working! No fix needed.")
        return 0
    
    # Try to fix permissions
    print("\n🔧 Attempting to fix microphone permissions...")
    if fix_microphone_permissions():
        print("\n✅ Permission fix instructions provided")
        print("   Please follow the steps above and restart the application")
    else:
        print("\n❌ Could not fix permissions automatically")
        print("   Please check Windows microphone settings manually")
    
    return 1

if __name__ == "__main__":
    sys.exit(main())
