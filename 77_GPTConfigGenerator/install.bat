@echo off
setlocal enabledelayedexpansion

echo Installing GPTConfigGenerator - Day 77 of #100DaysOfAI-Agents
echo.

REM Create and activate virtual environment
echo Creating virtual environment...
python -m venv venv
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated successfully.
) else (
    echo Failed to create virtual environment. Ensure Python is installed and on PATH.
    exit /b 1
)

REM Upgrade pip and install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy env.example .env
    echo Please edit .env file and add your API keys.
)

echo.
echo Installation complete! 
echo.
echo To start the application:
echo   1. Edit .env file and add your API keys
echo   2. Run: start.bat
echo   3. Open http://127.0.0.1:8000 in your browser
echo.
pause
