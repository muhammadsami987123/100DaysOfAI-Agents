@echo off
echo Installing SystemMonitorAgent...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not installed
    echo Please install pip and try again
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo.
echo Usage examples:
echo   python cli.py                     # Interactive CLI interface (recommended)
echo   python main.py                    # Monitor with default 5s interval
echo   python main.py -i 2              # Monitor with 2s interval
echo   python main.py --export json     # Export current stats
echo   python main.py --suggest         # Get AI optimization suggestions
echo   python main.py --health          # Get AI health assessment
echo.
echo For AI features, set OPENAI_API_KEY environment variable
echo.
pause
