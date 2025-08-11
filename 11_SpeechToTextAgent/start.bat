@echo off
echo Starting SpeechToTextAgent...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found. Please run install.bat first.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo Warning: .env file not found. Please create one with your OpenAI API key.
    echo.
    echo Example .env file content:
    echo OPENAI_API_KEY=sk-your-openai-api-key-here
    echo WHISPER_MODEL=whisper-1
    echo MAX_FILE_SIZE=25MB
    echo.
    pause
)

REM Activate virtual environment
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Start the application
echo Starting server on http://localhost:8010
echo Press Ctrl+C to stop the server
echo.
python server.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo Server stopped with error code: %errorlevel%
    pause
)
