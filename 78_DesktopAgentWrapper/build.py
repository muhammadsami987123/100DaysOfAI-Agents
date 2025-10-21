"""
Build script for creating executable packages
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """Build executable using PyInstaller"""
    print("🔨 Building DesktopAgentWrapper executable...")
    
    try:
        # Install PyInstaller if not already installed
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        
        # Build command
        build_cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name", "DesktopAgentWrapper",
            "--hidden-import", "customtkinter",
            "--hidden-import", "PIL",
            "--hidden-import", "openai",
            "--hidden-import", "google.generativeai",
            "main.py"
        ]
        
        # Add data directories if they exist
        if os.path.exists("agents"):
            build_cmd.insert(-1, "--add-data")
            build_cmd.insert(-1, "agents;agents")
        
        if os.path.exists("utils"):
            build_cmd.insert(-1, "--add-data")
            build_cmd.insert(-1, "utils;utils")
        
        if os.path.exists("assets"):
            build_cmd.insert(-1, "--add-data")
            build_cmd.insert(-1, "assets;assets")
        
        # Add icon if it exists
        if os.path.exists("assets/icon.ico"):
            build_cmd.insert(-1, "--icon")
            build_cmd.insert(-1, "assets/icon.ico")
        
        print(f"Running: {' '.join(build_cmd)}")
        result = subprocess.run(build_cmd, check=True)
        
        print("✅ Executable built successfully!")
        print("📁 Output: dist/DesktopAgentWrapper.exe")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def clean_build():
    """Clean build artifacts"""
    print("🧹 Cleaning build artifacts...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["*.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ Removed {dir_name}/")
    
    for pattern in files_to_clean:
        for file_path in Path(".").glob(pattern):
            file_path.unlink()
            print(f"✅ Removed {file_path}")

def main():
    """Main build process"""
    print("🖥️ DesktopAgentWrapper - Build Script")
    print("=" * 50)
    
    # Check if PyInstaller is available
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Clean previous builds
    clean_build()
    
    # Build executable
    if build_executable():
        print("\n🎉 Build completed successfully!")
        print("\n📋 Next steps:")
        print("1. Test the executable: dist/DesktopAgentWrapper.exe")
        print("2. Distribute the executable to users")
        print("3. Create installer if needed")
    else:
        print("\n❌ Build failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
