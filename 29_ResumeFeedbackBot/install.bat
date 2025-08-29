@echo off
echo ========================================
echo ResumeFeedbackBot Installation Script
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found!
echo.

echo Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install packages
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Creating .env file...
if not exist .env (
    echo Creating .env file with default settings...
    echo # ResumeFeedbackBot Configuration > .env
    echo OPENAI_API_KEY=your_openai_api_key_here >> .env
    echo OPENAI_MODEL=gpt-4 >> .env
    echo OPENAI_MAX_TOKENS=4000 >> .env
    echo OPENAI_TEMPERATURE=0.7 >> .env
    echo DEBUG=True >> .env
    echo HOST=127.0.0.1 >> .env
    echo PORT=5000 >> .env
    echo SECRET_KEY=resume-feedback-bot-secret-key-2024 >> .env
    echo.
    echo IMPORTANT: Please edit .env file and add your OpenAI API key
    echo You can get one from https://platform.openai.com/api-keys
) else (
    echo .env file already exists
)

echo.
echo Creating necessary directories...
if not exist uploads mkdir uploads
if not exist outputs mkdir outputs
if not exist logs mkdir logs

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo To start the web interface:
echo   python server.py
echo.
echo To use the CLI:
echo   python cli.py --help
echo.
echo Don't forget to:
echo 1. Add your OpenAI API key to the .env file
echo 2. Test the installation with: python cli.py interactive
echo.
pause
