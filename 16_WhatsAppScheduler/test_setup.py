#!/usr/bin/env python3
"""
WhatsApp Scheduler Setup Test Script
Run this to verify your installation and identify common issues.
"""

import sys
import os
import importlib

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.7+")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\n📦 Testing dependencies...")
    
    dependencies = [
        ('pywhatkit', 'pywhatkit'),
        ('json', 'json'),
        ('datetime', 'datetime'),
        ('threading', 'threading'),
        ('pathlib', 'pathlib'),
        ('re', 're')
    ]
    
    all_good = True
    for name, module in dependencies:
        try:
            importlib.import_module(module)
            print(f"✅ {name} - Available")
        except ImportError:
            print(f"❌ {name} - Missing")
            all_good = False
    
    return all_good

def test_pywhatkit_version():
    """Test pywhatkit version and features"""
    print("\n🔧 Testing pywhatkit...")
    
    try:
        import pywhatkit as pwk
        import pkg_resources
        
        version = pkg_resources.get_distribution("pywhatkit").version
        print(f"✅ pywhatkit version: {version}")
        
        # Check available methods
        has_instant = hasattr(pwk, 'sendwhatmsg_instantly')
        has_scheduled = hasattr(pwk, 'sendwhatmsg')
        
        print(f"   - sendwhatmsg_instantly: {'✅' if has_instant else '❌'}")
        print(f"   - sendwhatmsg: {'✅' if has_scheduled else '❌'}")
        
        if not has_instant and not has_scheduled:
            print("❌ No sending methods available!")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ pywhatkit test failed: {e}")
        return False

def test_browser_access():
    """Test browser accessibility"""
    print("\n🌐 Testing browser access...")
    
    try:
        import webbrowser
        browser = webbrowser.get()
        print(f"✅ Browser detected: {browser.name}")
        
        # Try to open a test URL
        try:
            browser.open('https://www.google.com')
            print("✅ Browser can open URLs")
            return True
        except Exception as e:
            print(f"⚠️  Browser URL opening test failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Browser access test failed: {e}")
        return False

def test_whatsapp_web_access():
    """Test WhatsApp Web accessibility"""
    print("\n📱 Testing WhatsApp Web access...")
    
    try:
        import urllib.request
        import urllib.error
        
        url = "https://web.whatsapp.com"
        try:
            response = urllib.request.urlopen(url, timeout=10)
            if response.status == 200:
                print("✅ WhatsApp Web is accessible")
                return True
            else:
                print(f"⚠️  WhatsApp Web returned status: {response.status}")
                return False
        except urllib.error.URLError as e:
            print(f"❌ WhatsApp Web not accessible: {e}")
            return False
            
    except Exception as e:
        print(f"❌ WhatsApp Web test failed: {e}")
        return False

def test_config_file():
    """Test configuration file"""
    print("\n⚙️  Testing configuration...")
    
    try:
        import config
        
        # Check essential config values
        required_configs = [
            'WHATSAPP_WEB_URL',
            'WAIT_TIME',
            'TAB_CLOSE',
            'DEFAULT_DELAY_SECONDS',
            'PHONE_NUMBER_REGEX'
        ]
        
        all_configs_good = True
        for config_name in required_configs:
            if hasattr(config, config_name):
                value = getattr(config, config_name)
                print(f"✅ {config_name}: {value}")
            else:
                print(f"❌ {config_name}: Missing")
                all_configs_good = False
        
        return all_configs_good
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_file_permissions():
    """Test file write permissions"""
    print("\n📁 Testing file permissions...")
    
    try:
        test_file = "test_permissions.tmp"
        
        # Try to write a test file
        with open(test_file, 'w') as f:
            f.write("test")
        
        # Try to read it back
        with open(test_file, 'r') as f:
            content = f.read()
        
        # Clean up
        os.remove(test_file)
        
        if content == "test":
            print("✅ File read/write permissions - OK")
            return True
        else:
            print("❌ File content verification failed")
            return False
            
    except Exception as e:
        print(f"❌ File permissions test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("🧪 WhatsApp Scheduler Setup Test")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("pywhatkit", test_pywhatkit_version),
        ("Browser Access", test_browser_access),
        ("WhatsApp Web", test_whatsapp_web_access),
        ("Configuration", test_config_file),
        ("File Permissions", test_file_permissions)
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
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup looks good.")
        print("💡 You can now run: python main.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("💡 Check the troubleshooting section in README.md")
        
        # Specific recommendations
        if not any(name == "pywhatkit" and result for name, result in results):
            print("\n🔧 To fix pywhatkit issues:")
            print("   pip install --upgrade pywhatkit")
            
        if not any(name == "Browser Access" and result for name, result in results):
            print("\n🌐 To fix browser issues:")
            print("   - Install Chrome browser")
            print("   - Make sure Chrome is in your PATH")
            
        if not any(name == "WhatsApp Web" and result for name, result in results):
            print("\n📱 To fix WhatsApp Web issues:")
            print("   - Check your internet connection")
            print("   - Try accessing web.whatsapp.com manually")

if __name__ == "__main__":
    run_all_tests()
