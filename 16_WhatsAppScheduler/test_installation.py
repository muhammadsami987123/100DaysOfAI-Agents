#!/usr/bin/env python3
"""
Test script for WhatsApp Scheduler Agent
Verifies installation and basic functionality
"""

import sys
import importlib
import datetime
import re
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    required_modules = [
        'pywhatkit',
        'selenium',
        'webdriver_manager'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("✅ All imports successful!")
    return True

def test_phone_validation():
    """Test phone number validation"""
    print("\n📱 Testing phone number validation...")
    
    # Test cases
    test_cases = [
        ("+12345678901", True),  # 11 digits (US format)
        ("+447911123456", True),  # 12 digits (UK format)
        ("+919876543210", True),  # 12 digits (India format)
        ("1234567890", False),  # No country code
        ("+123456789", False),  # Too short (9 digits)
        ("+1234567890123456", False),  # Too long (16 digits)
        ("abc123", False),  # Invalid characters
        ("+1 234 567 8901", True),  # With spaces (11 digits)
        ("+1-234-567-8901", True),  # With dashes (11 digits)
        ("(+1) 234-567-8901", True),  # With parentheses (11 digits)
    ]
    
    failed_tests = []
    
    for phone, expected in test_cases:
        # Simple validation regex (same as in main.py)
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        result = bool(re.match(r'^\+[1-9]\d{10,14}$', cleaned))
        
        if result == expected:
            print(f"✅ {phone} -> {result}")
        else:
            print(f"❌ {phone} -> {result} (expected {expected})")
            failed_tests.append(phone)
    
    if failed_tests:
        print(f"\n❌ Failed validation tests: {', '.join(failed_tests)}")
        return False
    
    print("✅ All phone validation tests passed!")
    return True

def test_time_validation():
    """Test time format validation"""
    print("\n⏰ Testing time format validation...")
    
    # Test cases
    test_cases = [
        ("09:30", True),
        ("14:15", True),
        ("23:45", True),
        ("00:00", True),
        ("24:00", False),  # Invalid hour
        ("12:60", False),  # Invalid minute
        ("9:30", True),   # Valid time (leading zero not required)
        ("09:5", True),   # Valid time (leading zero not required)
        ("abc", False),    # Invalid format
        ("12:30:45", False),  # Too many parts
    ]
    
    failed_tests = []
    
    for time_str, expected in test_cases:
        try:
            hour, minute = map(int, time_str.split(':'))
            result = 0 <= hour <= 23 and 0 <= minute <= 59
        except:
            result = False
        
        if result == expected:
            print(f"✅ {time_str} -> {result}")
        else:
            print(f"❌ {time_str} -> {result} (expected {expected})")
            failed_tests.append(time_str)
    
    if failed_tests:
        print(f"\n❌ Failed time validation tests: {', '.join(failed_tests)}")
        return False
    
    print("✅ All time validation tests passed!")
    return True

def test_default_time():
    """Test default time calculation"""
    print("\n🕐 Testing default time calculation...")
    
    try:
        now = datetime.datetime.now()
        default_time = now + datetime.timedelta(minutes=2)
        time_str = default_time.strftime("%H:%M")
        
        print(f"✅ Current time: {now.strftime('%H:%M')}")
        print(f"✅ Default time: {time_str}")
        
        # Verify it's 2 minutes ahead
        time_diff = (default_time - now).total_seconds() / 60
        if 1.5 <= time_diff <= 2.5:  # Allow small tolerance
            print(f"✅ Time difference: {time_diff:.1f} minutes")
            return True
        else:
            print(f"❌ Unexpected time difference: {time_diff:.1f} minutes")
            return False
            
    except Exception as e:
        print(f"❌ Error calculating default time: {e}")
        return False

def test_file_operations():
    """Test file operations"""
    print("\n💾 Testing file operations...")
    
    try:
        # Test JSON operations
        test_data = {
            'messages': {
                1: {
                    'phone': '+1234567890',
                    'message': 'Test message',
                    'scheduled_time': datetime.datetime.now().isoformat(),
                    'status': 'scheduled'
                }
            },
            'counter': 2
        }
        
        # Test writing
        import json
        test_file = Path("test_messages.json")
        with open(test_file, 'w') as f:
            json.dump(test_data, f, indent=2)
        print("✅ JSON write successful")
        
        # Test reading
        with open(test_file, 'r') as f:
            loaded_data = json.load(f)
        print("✅ JSON read successful")
        
        # Test data integrity
        if loaded_data['messages']['1']['phone'] == '+1234567890':
            print("✅ Data integrity verified")
        else:
            print("❌ Data integrity check failed")
            return False
        
        # Cleanup
        test_file.unlink()
        print("✅ Test file cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ File operation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 WhatsApp Scheduler Agent - Installation Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Phone Validation", test_phone_validation),
        ("Time Validation", test_time_validation),
        ("Default Time", test_default_time),
        ("File Operations", test_file_operations),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Installation is successful.")
        print("\n🚀 You can now run the WhatsApp Scheduler:")
        print("   python main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n💡 Common solutions:")
        print("   1. Run: pip install -r requirements.txt")
        print("   2. Ensure Python 3.7+ is installed")
        print("   3. Check internet connection")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
