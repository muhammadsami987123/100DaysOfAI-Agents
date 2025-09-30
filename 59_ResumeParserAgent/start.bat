@echo off
echo Starting ResumeParserAgent...
echo.

REM Check if .env file exists
if not exist .env (
    echo Warning: .env file not found
    echo Please copy env.example to .env and add your Google Gemini API key
    echo. 
)

python main.py
