@echo off
echo 📝 GPTNotepad - Starting...
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

REM Check if .env file exists and API keys are set
echo.
if not exist ".env" (
    echo ⚠️  No .env file found!
    echo OPENAI_MODEL=gpt-3.5-turbo
    echo LLM_MODEL=gemini
    echo GEMINI_API_KEY=your_gemini_api_key_here
    echo GEMINI_MODEL=gemini-2.0-flash
    echo DEBUG=True
    echo.
    echo 📝 Please create a .env file with your API keys (Gemini is default):
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('type .env ^| findstr /r "^OPENAI_API_KEY="') do set "OPENAI_API_KEY_CHECK=%%i"
    for /f "tokens=*" %%i in ('type .env ^| findstr /r "^GEMINI_API_KEY="') do set "GEMINI_API_KEY_CHECK=%%i"

    if "!OPENAI_API_KEY_CHECK!"=="OPENAI_API_KEY=" (
        echo ⚠️  OPENAI_API_KEY not set in .env file.
    )
    if "!GEMINI_API_KEY_CHECK!"=="GEMINI_API_KEY=" (
        echo ⚠️  GEMINI_API_KEY not set in .env file.
    )
    echo.
)

REM Start the application
echo.
echo 🚀 Starting GPTNotepad...
echo 📱 Open your browser and go to: http://localhost:8000
echo.
python main.py

pause
