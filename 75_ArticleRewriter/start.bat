@echo off
echo 📝 ArticleRewriter - Starting...
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
if not exist ".env" (
    echo.
    echo ⚠️  No .env file found!
    echo Please create a .env file with your API key:
    echo LLM_MODEL=gemini
    echo GEMINI_API_KEY=your_gemini_api_key_here
    echo OPENAI_API_KEY=your_openai_api_key_here
    echo DEBUG=True
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('type .env ^| findstr /r "^GEMINI_API_KEY="') do set "GEMINI_API_KEY_CHECK=%%i"
    for /f "tokens=*" %%i in ('type .env ^| findstr /r "^OPENAI_API_KEY="') do set "OPENAI_API_KEY_CHECK=%%i"

    if "!GEMINI_API_KEY_CHECK!"=="GEMINI_API_KEY=" (
        echo ⚠️  GEMINI_API_KEY not set in .env file.
    )
    if "!OPENAI_API_KEY_CHECK!"=="OPENAI_API_KEY=" (
        echo ⚠️  OPENAI_API_KEY not set in .env file.
    )
    echo.
)

REM Test installation
echo.
echo 🧪 Testing installation...
python test_installation.py

REM Start the application
echo.
echo 🚀 Starting ArticleRewriter...
echo 📱 Open your browser and go to: http://localhost:8075
echo.
python main.py

pause
