@echo off
setlocal

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else if exist venv\bin\activate (
    call venv\bin\activate
)

python cli.py %*

endlocal
