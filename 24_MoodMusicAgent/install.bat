@echo off
echo ========================================
echo MoodMusicAgent Installation Script
echo ========================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Creating necessary directories...
if not exist "data" mkdir data
if not exist "logs" mkdir logs

echo.
echo Copying environment template...
if not exist ".env" copy "env.example" ".env"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your API keys (optional)
echo 2. Run: python main.py
echo.
echo For help, see README.md
echo.
pause
