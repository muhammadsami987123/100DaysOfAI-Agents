@echo off
echo ========================================
echo Starting ResumeFeedbackBot Web Server
echo ========================================
echo.

echo Checking if .env file exists...
if not exist .env (
    echo ERROR: .env file not found!
    echo Please run install.bat first to create the configuration file
    echo Then add your OpenAI API key to the .env file
    pause
    exit /b 1
)

echo Checking if OpenAI API key is configured...
findstr /C:"OPENAI_API_KEY=your_openai_api_key_here" .env >nul
if not errorlevel 1 (
    echo ERROR: Please add your OpenAI API key to the .env file
    echo Replace 'your_openai_api_key_here' with your actual API key
    echo You can get one from https://platform.openai.com/api-keys
    pause
    exit /b 1
)

echo Configuration looks good!
echo.

echo Starting ResumeFeedbackBot server...
echo The web interface will be available at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.

python server.py

echo.
echo Server stopped.
pause
