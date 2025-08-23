@echo off
echo Installing AICommandExplainerAgent...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo Installing required packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install packages
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo.
echo Next steps:
echo 1. Create a .env file with your OPENAI_API_KEY
echo 2. Run: python main.py
echo.
pause
