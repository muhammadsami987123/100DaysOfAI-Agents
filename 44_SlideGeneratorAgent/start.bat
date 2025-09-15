@echo off
cd /d %~dp0
call venv\Scripts\activate
if exist .env (
  for /f "usebackq tokens=1,2 delims==" %%a in (".env") do set %%a=%%b
)
python main.py
pause


