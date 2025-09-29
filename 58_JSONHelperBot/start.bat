@echo off
echo Starting JSONHelperBot...
echo.

REM Check if .env file exists
if not exist .env (
    echo Warning: .env file not found
    echo Please copy env.example to .env and add your OpenAI API key
    echo. 
)

python main.py --menu
