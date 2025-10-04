import sys
import importlib
import os

def test_python_version():
    """Test if the Python version is compatible."""
    print(f"🐍 Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required.")
        return False
    else:
        print("✅ Python version is compatible.")
        return True

def test_imports():
    """Test if all required packages can be imported."""
    required_packages = [
        'fastapi',
        'uvicorn',
        'google.generativeai',
        'python_dotenv',
        'pydantic',
        'jinja2'
    ]
    
    print("\n🔍 Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    return not bool(failed_imports)

def test_config():
    """Test configuration loading and API key presence."""
    print("\n🔧 Testing configuration...")
    try:
        from config import Config
        print("✅ Configuration module imported.")
        
        if Config.GOOGLE_API_KEY:
            print("✅ Google API key found (in .env or env var).")
        else:
            print("⚠️ Google API key not found. Please set GOOGLE_API_KEY in your .env file.")
            return False # Fail if API key is not set
        
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_ai_agent():
    """Test AI agent initialization."""
    print("\n🤖 Testing AI agent initialization...")
    try:
        from ai_agent import AIQuoteGenerator
        agent = AIQuoteGenerator()
        if agent.client:
            print("✅ AIQuoteGenerator initialized with Google Gemini.")
        else:
            print("⚠️ AIQuoteGenerator initialized without Gemini (limited functionality).")
            print("   Please check your Google API key and internet connection.")
        return True
    except Exception as e:
        print(f"❌ AI agent initialization failed: {e}")
        return False

def test_fastapi_app():
    """Test FastAPI application import."""
    print("\n🚀 Testing FastAPI application...")
    try:
        from main import app
        print("✅ FastAPI app imported.")
        print(f"✅ App title: {app.title}")
        return True
    except Exception as e:
        print(f"❌ FastAPI app import failed: {e}")
        return False

def test_file_structure():
    """Test if essential directories and files exist."""
    print("\n📁 Testing file structure...")
    base_dir = os.path.dirname(__file__)
    required_dirs = [
        os.path.join(base_dir, "templates"),
        os.path.join(base_dir, "static", "js"),
        os.path.join(base_dir, "static", "css"),
    ]
    required_files = [
        os.path.join(base_dir, "main.py"),
        os.path.join(base_dir, "config.py"),
        os.path.join(base_dir, "ai_agent.py"),
        os.path.join(base_dir, "requirements.txt"),
        os.path.join(base_dir, "install.bat"),
        os.path.join(base_dir, "start.bat"),
        os.path.join(base_dir, "README.md"),
    ]

    all_present = True

    for d in required_dirs:
        if not os.path.isdir(d):
            print(f"❌ Missing directory: {d}")
            all_present = False
        else:
            print(f"✅ Found directory: {d}")

    for f in required_files:
        if not os.path.isfile(f):
            print(f"❌ Missing file: {f}")
            all_present = False
        else:
            print(f"✅ Found file: {f}")
            
    # Check for template files and static assets (these might be created later)
    if not os.path.isfile(os.path.join(base_dir, "templates", "index.html")):
        print("⚠️  templates/index.html not found. This will be created later.")
    else:
        print("✅ Found templates/index.html.")
        
    if not os.path.isfile(os.path.join(base_dir, "static", "js", "app.js")):
        print("⚠️  static/js/app.js not found. This will be created later.")
    else:
        print("✅ Found static/js/app.js.")

    return all_present

def main():
    """Run all installation tests."""
    print("🌟 AIQuoteGenerator - Installation Test")
    print("=" * 50)

    results = [
        test_python_version(),
        test_imports(),
        test_config(),
        test_ai_agent(),
        test_fastapi_app(),
        test_file_structure()
    ]

    print("\n" + "=" * 50)
    if all(results):
        print("🎉 All essential tests passed! AIQuoteGenerator is ready to run.")
        print("\n📋 Next steps:")
        print("1. Ensure your Google Gemini API key is set in the .env file.")
        print("2. Run: python main.py")
        print("3. Open your browser to: http://localhost:8000")
        return True
    else:
        print("❌ Some tests failed. Please review the output above and resolve any issues.")
        print("   Refer to README.md for troubleshooting steps.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
