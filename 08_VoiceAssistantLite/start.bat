@echo off
REM VoiceAssistantLite - Start script (Windows)
cd /d %~dp0
call venv\Scripts\activate
python main.py
pause


