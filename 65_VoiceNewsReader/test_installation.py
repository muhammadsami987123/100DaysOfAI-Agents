import importlib
from config import Config


def main() -> bool:
    print("🗞️ VoiceNewsReader - Installation Test")
    try:
        for pkg in [
            "fastapi",
            "uvicorn",
            "requests",
            "jinja2",
        ]:
            importlib.import_module(pkg)
            print(f"✅ {pkg}")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

    try:
        Config.validate()
        print("✅ Config validated")
    except Exception as e:
        print(f"⚠️ Config warning: {e}")

    try:
        from main import app  # noqa: F401
        print("✅ FastAPI app import OK")
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

    print("🎉 All checks passed")
    return True


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)


