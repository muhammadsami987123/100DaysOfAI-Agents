@echo off
setlocal
call venv\Scripts\activate
python main.py %*
endlocal

