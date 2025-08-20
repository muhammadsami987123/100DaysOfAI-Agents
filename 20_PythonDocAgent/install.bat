@echo off
echo ========================================
echo PythonDocAgent - Day 20 Installation
echo ========================================
echo.

echo Creating virtual environment...
python -m venv venv

if exist venv\Scripts\activate.bat (
	echo Activating virtual environment...
	call venv\Scripts\activate
) else (
	echo Failed to create venv. Ensure Python is installed and on PATH.
	exit /b 1
)

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo Next steps:
echo 1. Copy env.example to .env and fill values

echo 2. Run: start.bat --help
pause > nul
