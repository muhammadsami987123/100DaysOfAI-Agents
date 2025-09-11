@echo off
echo Starting CryptoInsightsAgent...
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Please run install.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Run the agent
echo Running CryptoInsightsAgent...
python main.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Agent exited with an error.
    pause
)
