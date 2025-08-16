@echo off
echo Installing WhatsApp Scheduler Agent...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
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
echo Installation completed successfully!
echo.
echo To run the WhatsApp Scheduler:
echo   python main.py
echo.
echo Make sure to:
echo   1. Open WhatsApp Web in your browser
echo   2. Log in with your phone
echo   3. Keep the browser tab open
echo.
pause
