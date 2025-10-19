@echo off
setlocal enabledelayedexpansion

if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    python main.py
) else (
    echo Virtual environment not found. Run install.bat first.
    exit /b 1
)
