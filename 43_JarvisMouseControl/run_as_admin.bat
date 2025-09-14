@echo off
echo ========================================
echo JarvisMouseControl - Run as Administrator
echo ========================================
echo.
echo This script will run JarvisMouseControl with administrator privileges
echo to ensure microphone access works properly.
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorlevel% == 0 (
    echo Running as administrator - Good!
    echo.
    goto :run_app
) else (
    echo Not running as administrator. Restarting with admin privileges...
    echo.
    powershell -Command "Start-Process cmd -ArgumentList '/c cd /d %~dp0 && %~f0' -Verb RunAs"
    exit /b
)

:run_app
echo Starting JarvisMouseControl with full permissions...
echo.

REM Set environment variables
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1

REM Set parent directory virtual environment path
set PARENT_VENV=..\venv

REM Check if parent virtual environment exists
if exist "%PARENT_VENV%\Scripts\activate.bat" (
    echo Activating parent virtual environment...
    call "%PARENT_VENV%\Scripts\activate.bat"
    echo Parent virtual environment activated.
) else (
    echo Parent virtual environment not found. Creating one...
    python -m venv "%PARENT_VENV%"
    call "%PARENT_VENV%\Scripts\activate.bat"
    echo Installing dependencies...
    pip install -r requirements.txt
    echo Parent virtual environment created and dependencies installed.
)

echo.

REM Run the application with improved startup
python start.py

echo.
echo JarvisMouseControl has stopped.
pause
