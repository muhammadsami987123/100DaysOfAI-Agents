@echo off
echo Starting AICommandExplainerAgent...
echo.

REM Check if .env file exists
if not exist .env (
    echo Warning: .env file not found
    echo Please create a .env file with your OPENAI_API_KEY
    echo.
    echo Example .env file content:
    echo OPENAI_API_KEY=your_api_key_here
    echo.
    pause
)

REM Check if required packages are installed
python -c "import openai, rich, dotenv" >nul 2>&1
if errorlevel 1 (
    echo Error: Required packages not installed
    echo Please run install.bat first
    pause
    exit /b 1
)

echo Starting the agent...
python main.py

pause
