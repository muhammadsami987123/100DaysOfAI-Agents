@echo off
echo 🤖 VoiceNoteAgent - Installation Script
echo ======================================
echo.

echo 📋 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo 💡 Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

echo 🔧 Installing dependencies...
echo.

echo 📦 Installing pipwin (for Windows PyAudio support)...
pip install pipwin

echo 📦 Installing PyAudio...
pipwin install pyaudio

echo 📦 Installing other dependencies...
pip install -r requirements.txt

echo.
echo ✅ Installation completed!
echo.
echo 🚀 To start VoiceNoteAgent, run:
echo    python main.py
echo.
echo 🧪 To run tests, use:
echo    python test_agent.py
echo.
echo 🔍 To check system, use:
echo    python config.py check
echo.
pause 