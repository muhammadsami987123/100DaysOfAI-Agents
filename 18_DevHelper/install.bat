@echo off
setlocal enabledelayedexpansion

REM Create and activate virtual environment
python -m venv venv
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Failed to create virtual environment. Ensure Python is installed and on PATH.
    exit /b 1
)

REM Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Installation complete. To start:
echo.
echo   call venv\Scripts\activate
echo   python main.py
