@echo off
setlocal enabledelayedexpansion

echo Starting GPTConfigGenerator - Day 77 of #100DaysOfAI-Agents
echo.

if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
    echo.
    echo Starting the application...
    echo Open http://127.0.0.1:8000 in your browser
    echo.
    python main.py
) else (
    echo Virtual environment not found. Please run install.bat first.
    echo.
    pause
    exit /b 1
)
