@echo off
echo 🌍 Location Info Agent - Starting...
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
    echo Please create a .env file with your OpenAI, Google Maps, and Image Search API keys:
    echo OPENAI_API_KEY=your_openai_api_key_here
    echo GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
    echo IMAGE_SEARCH_API_KEY=your_image_search_api_key_here
    echo TTS_ENGINE=openai
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('type .env ^| findstr /r "^OPENAI_API_KEY="') do set "OPENAI_API_KEY_CHECK=%%i"
    for /f "tokens=*" %%i in ('type .env ^| findstr /r "^GOOGLE_MAPS_API_KEY="') do set "GOOGLE_MAPS_API_KEY_CHECK=%%i"
    for /f "tokens=*" %%i in ('type .env ^| findstr /r "^IMAGE_SEARCH_API_KEY="') do set "IMAGE_SEARCH_API_KEY_CHECK=%%i"

    if "!OPENAI_API_KEY_CHECK!"=="OPENAI_API_KEY=" (
        echo ⚠️  OPENAI_API_KEY not set in .env file. AI features will be limited.
    )
    if "!GOOGLE_MAPS_API_KEY_CHECK!"=="GOOGLE_MAPS_API_KEY=" (
        echo ⚠️  GOOGLE_MAPS_API_KEY not set in .env file. Map features will be disabled.
    )
    if "!IMAGE_SEARCH_API_KEY_CHECK!"=="IMAGE_SEARCH_API_KEY=" (
        echo ⚠️  IMAGE_SEARCH_API_KEY not set in .env file. Image features will be disabled.
    )
    echo.
)

REM Test installation
echo.
echo 🧪 Testing installation...
python test_installation.py

REM Start the application
echo.
echo 🚀 Starting Location Info Agent...
echo 📱 Open your browser and go to: http://localhost:8000
echo.
python main.py

pause
