@echo off
echo ========================================
echo TextFixer Assistant - Day 21 Installation
echo ========================================
echo.

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Creating example .env if not present...
if not exist .env (
  copy env.example .env > nul
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env to configure provider and API keys
echo 2. Run: start.bat
echo.
echo Press any key to exit...
pause > nul

