@echo off
echo ========================================
echo StudyPlannerAgent - Startup Script
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found
    echo Please run install.bat first to set up the environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if OpenAI API key is set
if "%OPENAI_API_KEY%"=="" (
    echo WARNING: OpenAI API key not found in environment variables
    echo.
    echo Please set your API key:
    echo 1. Get your API key from: https://platform.openai.com/api-keys
    echo 2. Set it using: set OPENAI_API_KEY=your_api_key_here
    echo 3. Or create a .env file with: OPENAI_API_KEY=your_api_key_here
    echo.
    echo The application will still start, but you'll need to set the API key
    echo before generating study plans.
    echo.
    pause
)

echo Starting StudyPlannerAgent...
echo.
echo Choose your preferred interface:
echo 1. Web Interface (default) - http://127.0.0.1:8042
echo 2. Terminal Interface
echo 3. Quick Plan Generation
echo.

set /p choice="Enter your choice (1-3, default: 1): "

if "%choice%"=="2" (
    echo Starting Terminal Interface...
    python main.py --terminal
) else if "%choice%"=="3" (
    set /p goal="Enter your study goal: "
    if "%goal%"=="" (
        echo No goal provided. Starting web interface instead...
        python main.py --web
    ) else (
        echo Generating quick study plan for: %goal%
        python main.py --quick "%goal%"
    )
) else (
    echo Starting Web Interface...
    echo.
    echo StudyPlannerAgent will open in your default browser
    echo If it doesn't open automatically, go to: http://127.0.0.1:8042
    echo.
    echo Press Ctrl+C to stop the server
    echo.
    
    REM Start the web interface
    python main.py --web
    
    REM Open browser after a short delay
    timeout /t 3 /nobreak >nul
    start http://127.0.0.1:8042
)

echo.
echo StudyPlannerAgent has stopped.
pause
