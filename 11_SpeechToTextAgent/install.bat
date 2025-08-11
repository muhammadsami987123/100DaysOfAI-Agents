@echo off
echo Installing SpeechToTextAgent dependencies...
echo.

REM Create virtual environment
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install dependencies
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo.
echo Next steps:
echo 1. Create a .env file with your OpenAI API key
echo 2. Run start.bat to start the application
echo.
pause
