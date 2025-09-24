# test_installation.py
"""
Test script to verify PhotoOrganizerAgent installation and environment.
"""
import os
import sys

def test_env():
    assert sys.version_info >= (3, 8), "Python 3.8+ required."
    assert os.path.exists('requirements.txt'), "requirements.txt missing."
    print("[PASS] Environment and files check.")

def test_imports():
    try:
        import click
        import fastapi
        import dotenv
    except ImportError as e:
        print(f"[FAIL] Missing dependency: {e}")
        return False
    print("[PASS] All dependencies importable.")
    return True

def run_all():
    test_env()
    assert test_imports(), "Dependency import failed."
    print("All installation tests passed.")

if __name__ == "__main__":
    run_all()
