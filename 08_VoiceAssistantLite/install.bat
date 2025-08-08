@echo off
REM VoiceAssistantLite - Windows quick install
cd /d %~dp0
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
echo Installation complete. Edit .env (copy from README settings) if needed.
pause


