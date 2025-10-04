@echo off
echo 🌟 AIQuoteGenerator - Starting...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Please run install.bat first to set up the environment.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  No .env file found!
    echo Creating .env file template...
    echo GOOGLE_API_KEY=your_gemini_api_key_here > .env
    echo.
    echo 📝 Please edit the .env file and add your Google Gemini API key
    echo Then run this script again.
    pause
    exit /b 1
)

REM Start the application
echo.
echo 🚀 Starting AIQuoteGenerator...
echo 📱 Open your browser and go to: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
