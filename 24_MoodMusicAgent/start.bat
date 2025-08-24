@echo off
echo ========================================
echo Starting MoodMusicAgent...
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Checking dependencies...
python -c "import pygame, textblob, nltk" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Some dependencies may not be installed
    echo Run install.bat first if you haven't already
    echo.
    pause
)

echo.
echo Launching MoodMusicAgent...
echo.
python main.py

echo.
echo MoodMusicAgent has exited.
pause
