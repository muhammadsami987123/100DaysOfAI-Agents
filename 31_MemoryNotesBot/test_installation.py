#!/usr/bin/env python3
"""
MemoryNotesBot Installation Test
Run this script to verify that all components are working correctly
"""

import sys
import os
import json
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing module imports...")
    
    try:
        from config import Config
        print("✅ Config module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Config: {e}")
        return False
    
    try:
        from models import Memory, MemoryType, MemoryPriority
        print("✅ Models module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Models: {e}")
        return False
    
    try:
        from memory_store import MemoryStore
        print("✅ MemoryStore module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import MemoryStore: {e}")
        return False
    
    try:
        from ai_service import AIService
        print("✅ AIService module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import AIService: {e}")
        return False
    
    try:
        from voice_service import VoiceService
        print("✅ VoiceService module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import VoiceService: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import Config
        
        # Test directory creation
        Config.create_directories()
        
        # Check if directories exist
        if os.path.exists(Config.DATA_DIR):
            print("✅ Data directory created successfully")
        else:
            print("❌ Data directory creation failed")
            return False
        
        if os.path.exists(Config.EXPORT_DIR):
            print("✅ Export directory created successfully")
        else:
            print("❌ Export directory creation failed")
            return False
        
        print(f"✅ Configuration loaded: {Config.APP_NAME} v{Config.VERSION}")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_memory_store():
    """Test memory storage functionality"""
    print("\n💾 Testing memory storage...")
    
    try:
        from memory_store import MemoryStore
        from models import Memory, MemoryType, MemoryPriority
        
        # Initialize memory store
        memory_store = MemoryStore()
        print("✅ Memory store initialized successfully")
        
        # Test memory creation
        test_memory = memory_store.add_memory(
            content="Test memory for installation verification",
            memory_type=MemoryType.LONG_TERM,
            priority=MemoryPriority.MEDIUM,
            tags=["test", "installation"],
            category="testing"
        )
        
        if test_memory and test_memory.id:
            print("✅ Memory creation test passed")
        else:
            print("❌ Memory creation test failed")
            return False
        
        # Test memory retrieval
        retrieved_memory = memory_store.get_memory(test_memory.id)
        if retrieved_memory and retrieved_memory.content == test_memory.content:
            print("✅ Memory retrieval test passed")
        else:
            print("❌ Memory retrieval test failed")
            return False
        
        # Test memory search
        search_results = memory_store.search_memories("test memory")
        if search_results and len(search_results) > 0:
            print("✅ Memory search test passed")
        else:
            print("❌ Memory search test failed")
            return False
        
        # Test statistics
        stats = memory_store.get_stats()
        if stats and stats.total_memories > 0:
            print("✅ Memory statistics test passed")
        else:
            print("❌ Memory statistics test failed")
            return False
        
        # Clean up test memory
        memory_store.delete_memory(test_memory.id)
        print("✅ Memory cleanup test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Memory store test failed: {e}")
        return False

def test_ai_service():
    """Test AI service functionality"""
    print("\n🤖 Testing AI service...")
    
    try:
        from ai_service import AIService
        
        ai_service = AIService()
        
        if ai_service.is_available():
            print("✅ AI service is available (OpenAI API key found)")
            
            # Test AI enhancement
            enhancement = ai_service.enhance_memory_content("Test content for AI enhancement")
            if enhancement:
                print("✅ AI enhancement test passed")
            else:
                print("⚠️  AI enhancement test failed (but service is available)")
        else:
            print("⚠️  AI service not available (no OpenAI API key)")
            print("   This is normal if you haven't set up your API key yet")
        
        return True
        
    except Exception as e:
        print(f"❌ AI service test failed: {e}")
        return False

def test_voice_service():
    """Test voice service functionality"""
    print("\n🎤 Testing voice service...")
    
    try:
        from voice_service import VoiceService
        
        voice_service = VoiceService()
        
        # Test voice status
        status = voice_service.get_voice_status()
        if status:
            print("✅ Voice service status retrieved")
            
            if status.get("tts_available"):
                print("✅ Text-to-speech is available")
            else:
                print("⚠️  Text-to-speech not available")
            
            if status.get("voice_enabled"):
                print("✅ Voice features are enabled")
            else:
                print("⚠️  Voice features are disabled")
        else:
            print("❌ Voice service status test failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Voice service test failed: {e}")
        return False

def test_web_app():
    """Test web application functionality"""
    print("\n🌐 Testing web application...")
    
    try:
        from web_app import app
        
        # Test if Flask app can be created
        if app and hasattr(app, 'route'):
            print("✅ Flask web application created successfully")
        else:
            print("❌ Flask web application creation failed")
            return False
        
        # Test if routes are registered
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        if routes:
            print(f"✅ Web routes registered: {len(routes)} routes found")
        else:
            print("❌ No web routes found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Web application test failed: {e}")
        return False

def test_cli():
    """Test CLI functionality"""
    print("\n💻 Testing CLI interface...")
    
    try:
        from cli import MemoryNotesBotCLI
        
        # Test CLI initialization
        cli = MemoryNotesBotCLI()
        print("✅ CLI interface initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI interface test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧠 MemoryNotesBot Installation Test")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_configuration),
        ("Memory Store", test_memory_store),
        ("AI Service", test_ai_service),
        ("Voice Service", test_voice_service),
        ("Web Application", test_web_app),
        ("CLI Interface", test_cli)
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
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MemoryNotesBot is ready to use.")
        print("\nNext steps:")
        print("1. Run: python main.py --demo (to add sample data)")
        print("2. Run: python main.py --cli (for command line interface)")
        print("3. Run: python main.py --web (for web interface)")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check if Python version is 3.8 or higher")
        print("3. Verify file permissions and directory access")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
