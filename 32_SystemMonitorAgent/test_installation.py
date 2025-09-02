"""
Test script to verify SystemMonitorAgent installation
"""
import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing module imports...")
    
    try:
        import psutil
        print("✓ psutil imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import psutil: {e}")
        return False
    
    try:
        import colorama
        print("✓ colorama imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import colorama: {e}")
        return False
    
    try:
        from config import DEFAULT_REFRESH_INTERVAL, DEFAULT_ALERT_THRESHOLDS
        print("✓ config module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import config: {e}")
        return False
    
    try:
        from utils import Colors, format_bytes, format_percentage
        print("✓ utils module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import utils: {e}")
        return False
    
    try:
        from monitor import SystemMonitor
        print("✓ monitor module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import monitor: {e}")
        return False
    
    try:
        from ai_assistant import AIAssistant
        print("✓ ai_assistant module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ai_assistant: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic monitoring functionality"""
    print("\nTesting basic functionality...")
    
    try:
        from monitor import SystemMonitor
        monitor = SystemMonitor()
        print("✓ SystemMonitor instance created successfully")
        
        # Test getting system stats
        stats = monitor.get_system_stats()
        if stats and 'timestamp' in stats:
            print("✓ System stats collected successfully")
        else:
            print("✗ Failed to collect system stats")
            return False
        
        # Test CPU stats
        cpu_stats = monitor.get_cpu_stats()
        if 'usage_percent' in cpu_stats:
            print("✓ CPU stats collected successfully")
        else:
            print("✗ Failed to collect CPU stats")
            return False
        
        # Test memory stats
        memory_stats = monitor.get_memory_stats()
        if 'usage_percent' in memory_stats:
            print("✓ Memory stats collected successfully")
        else:
            print("✗ Failed to collect memory stats")
            return False
        
        # Test disk stats
        disk_stats = monitor.get_disk_stats()
        if 'usage_percent' in disk_stats:
            print("✓ Disk stats collected successfully")
        else:
            print("✗ Failed to collect disk stats")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def test_ai_assistant():
    """Test AI assistant functionality"""
    print("\nTesting AI assistant...")
    
    try:
        from ai_assistant import AIAssistant
        ai = AIAssistant()
        
        if ai.is_available:
            print("✓ AI Assistant available (OpenAI API key found)")
        else:
            print("ℹ AI Assistant not available (no OpenAI API key)")
        
        print("✓ AI Assistant module loaded successfully")
        return True
        
    except Exception as e:
        print(f"✗ AI Assistant test failed: {e}")
        return False

def test_utils():
    """Test utility functions"""
    print("\nTesting utility functions...")
    
    try:
        from utils import format_bytes, format_percentage, format_resource_bar
        
        # Test format_bytes
        test_bytes = 1024 * 1024 * 1024  # 1 GB
        formatted = format_bytes(test_bytes)
        if "GB" in formatted:
            print("✓ format_bytes working correctly")
        else:
            print("✗ format_bytes not working correctly")
            return False
        
        # Test format_percentage
        test_percent = 85.5
        formatted = format_percentage(test_percent)
        if "85.5%" in formatted:
            print("✓ format_percentage working correctly")
        else:
            print("✗ format_percentage not working correctly")
            return False
        
        # Test format_resource_bar
        test_bar = format_resource_bar(75.0)
        if "█" in test_bar and "░" in test_bar:
            print("✓ format_resource_bar working correctly")
        else:
            print("✗ format_resource_bar not working correctly")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Utils test failed: {e}")
        return False

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from config import DEFAULT_REFRESH_INTERVAL, DEFAULT_ALERT_THRESHOLDS
        
        if DEFAULT_REFRESH_INTERVAL == 5:
            print("✓ Default refresh interval loaded correctly")
        else:
            print("✗ Default refresh interval incorrect")
            return False
        
        if all(key in DEFAULT_ALERT_THRESHOLDS for key in ['cpu', 'ram', 'disk']):
            print("✓ Alert thresholds loaded correctly")
        else:
            print("✗ Alert thresholds missing or incorrect")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("SystemMonitorAgent Installation Test")
    print("=" * 40)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_config),
        ("Utility Functions", test_utils),
        ("Basic Functionality", test_basic_functionality),
        ("AI Assistant", test_ai_assistant)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"✗ {test_name} test failed")
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! SystemMonitorAgent is ready to use.")
        print("\nQuick start:")
        print("  python main.py --single          # Test single snapshot")
        print("  python main.py                   # Start monitoring")
        print("  python main.py --help            # View all options")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("Try running: pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
