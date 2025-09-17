@echo off
call venv\Scripts\activate

REM Start Tailwind CSS watcher in a new console
start cmd /k "npm run dev --prefix .\"

python main.py
pause
