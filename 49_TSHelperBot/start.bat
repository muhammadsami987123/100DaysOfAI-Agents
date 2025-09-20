@echo off
echo Starting TSHelperBot...
echo.

REM Check if .env file exists
if not exist .env (
    echo Warning: .env file not found
    echo Please copy env.example to .env and add your OpenAI API key
    echo.
)

python agent.py --menu
