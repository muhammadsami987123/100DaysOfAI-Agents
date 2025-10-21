@echo off
echo 🖥️ DesktopAgentWrapper - Starting...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies (ensure they are up-to-date)
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo ⚠️  No .env file found!
    echo Creating .env file from template...
    copy env.example .env
    echo.
    echo 📝 Please edit the .env file and add your API keys
    echo.
    pause
)

REM Start the application
echo.
echo 🚀 Starting DesktopAgentWrapper...
echo.
python main.py

pause
