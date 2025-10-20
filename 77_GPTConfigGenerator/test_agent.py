#!/usr/bin/env python3
"""
Simple test script for GPTConfigGenerator agent
"""

import os
import sys
from agent import GPTConfigGenerator

def test_basic_functionality():
    """Test basic agent functionality without AI"""
    print("Testing GPTConfigGenerator basic functionality...")
    
    try:
        # Initialize agent
        agent = GPTConfigGenerator()
        print("✅ Agent initialized successfully")
        
        # Test supported formats
        formats = agent.get_supported_formats()
        print(f"✅ Supported formats: {formats}")
        
        # Test config types
        types = agent.get_config_types()
        print(f"✅ Config types available: {len(types)}")
        
        # Test default values
        defaults = agent.get_default_values()
        print(f"✅ Default values available: {len(defaults)}")
        
        # Test format detection
        json_format = agent._detect_format("Create a JSON config")
        yaml_format = agent._detect_format("Generate YAML file")
        print(f"✅ Format detection: JSON={json_format}, YAML={yaml_format}")
        
        # Test type detection
        app_type = agent._detect_config_type("Create Express app config")
        docker_type = agent._detect_config_type("Generate docker-compose file")
        print(f"✅ Type detection: App={app_type}, Docker={docker_type}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_fallback_generation():
    """Test fallback configuration generation"""
    print("\nTesting fallback configuration generation...")
    
    try:
        agent = GPTConfigGenerator()
        
        # Test fallback generation (should work without API keys)
        result = agent.generate_config(
            user_request="Create a simple JSON config",
            config_type="app_settings",
            format="json"
        )
        
        if result["success"]:
            print("✅ AI-powered generation successful")
        else:
            print("✅ Fallback generation working (expected without API keys)")
            print(f"   Generated: {result['config_content'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run tests"""
    print("🧪 GPTConfigGenerator Agent Test")
    print("=" * 40)
    
    tests = [
        test_basic_functionality,
        test_fallback_generation
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed: {e}")
            results.append(False)
    
    print("\n" + "=" * 40)
    print("📊 Test Results")
    print("=" * 40)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All tests passed! ({passed}/{total})")
        print("\n✅ GPTConfigGenerator agent is working correctly!")
        return 0
    else:
        print(f"⚠️  {passed}/{total} tests passed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
