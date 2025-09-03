@echo off
echo.
echo ========================================
echo    AI Quiz Maker - Starting Web UI
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ERROR: Virtual environment not found
    echo Please run install.bat first
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if OpenAI API key is set
if "%OPENAI_API_KEY%"=="" (
    echo.
    echo WARNING: OPENAI_API_KEY environment variable is not set
    echo.
    echo Please set your API key:
    echo   set OPENAI_API_KEY=your_api_key_here
    echo.
    echo Or create a .env file in your home directory with:
    echo   OPENAI_API_KEY=your_api_key_here
    echo.
    echo Get your API key from: https://platform.openai.com/api-keys
    echo.
    echo Press any key to continue anyway (may fail if no API key)...
    pause >nul
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import openai, flask" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Dependencies not installed
    echo Please run install.bat first
    echo.
    pause
    exit /b 1
)

echo.
echo Starting AI Quiz Maker Web Server...
echo.
echo The web interface will be available at:
echo   http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask server
python server.py

echo.
echo Server stopped.
pause
