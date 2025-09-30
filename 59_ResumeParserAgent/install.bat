@echo off
echo Installing ResumeParserAgent...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Installation complete!
echo.
echo To get started:
echo 1. Copy env.example to .env
echo 2. Add your Google Gemini API key to .env
echo 3. Run: python main.py
echo.
pause
