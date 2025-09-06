@echo off
echo ========================================
echo    StoryWriterAgent - Day 36
echo ========================================
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
    echo OPENAI_API_KEY=your_openai_api_key_here > .env
    echo.
    echo 📝 Please edit the .env file and add your OpenAI API key
    echo Then run this script again.
    pause
    exit /b 1
)

REM Start the application
echo.
echo 🚀 Starting StoryWriterAgent...
echo.
echo 📚 Web Interface: http://localhost:8036
echo 📚 Terminal Mode: python main.py --terminal
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py --web

pause
