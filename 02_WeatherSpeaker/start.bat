@echo off
echo 🌤️ Weather Speaker Agent - Starting...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo ⚠️  No .env file found!
    echo Please create a .env file with your OpenAI API key:
    echo OPENAI_API_KEY=your_api_key_here
    echo.
    pause
    exit /b 1
)

REM Test installation
echo.
echo Testing installation...
python test_installation.py

REM Start the application
echo.
echo 🚀 Starting Weather Speaker Agent...
echo 📱 Open your browser and go to: http://localhost:8000
echo.
python main.py

pause 