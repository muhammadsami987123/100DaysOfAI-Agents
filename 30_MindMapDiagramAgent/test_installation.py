#!/usr/bin/env python3
"""
Test script to verify MindMapDiagramAgent installation
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {package_name or module_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {package_name or module_name} - FAILED: {e}")
        return False

def main():
    print("🧠 MindMapDiagramAgent - Installation Test")
    print("=" * 50)
    
    # Core dependencies
    core_modules = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("openai", "OpenAI"),
        ("dotenv", "python-dotenv"),
        ("multipart", "python-multipart"),
        ("aiofiles", "aiofiles"),
        ("jinja2", "Jinja2"),
    ]
    
    # Export dependencies
    export_modules = [
        ("matplotlib", "Matplotlib"),
        ("networkx", "NetworkX"),
        ("PIL", "Pillow"),
        ("reportlab", "ReportLab"),
    ]
    
    print("\n📦 Core Dependencies:")
    core_success = all(test_import(module, name) for module, name in core_modules)
    
    print("\n🎨 Export Dependencies:")
    export_success = all(test_import(module, name) for module, name in export_modules)
    
    # Test local modules
    print("\n🏠 Local Modules:")
    local_success = True
    
    try:
        from config import Config
        print("✅ Config - OK")
    except ImportError as e:
        print(f"❌ Config - FAILED: {e}")
        local_success = False
    
    try:
        from mindmap_agent import MindMapAgent
        print("✅ MindMapAgent - OK")
    except ImportError as e:
        print(f"❌ MindMapAgent - FAILED: {e}")
        local_success = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    if core_success and export_success and local_success:
        print("🎉 All tests passed! MindMapDiagramAgent is ready to use.")
        print("\n🚀 To start the application:")
        print("   python server.py")
        print("   Then open http://127.0.0.1:8030 in your browser")
        return True
    else:
        print("⚠️  Some tests failed. Please check the installation.")
        if not core_success:
            print("   - Install core dependencies: pip install -r requirements.txt")
        if not export_success:
            print("   - Install export dependencies: pip install matplotlib networkx Pillow reportlab")
        if not local_success:
            print("   - Check that all Python files are in the correct location")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
