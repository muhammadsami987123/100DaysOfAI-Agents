@echo off
cd /d %~dp0
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
echo Installed. Create .env with OPENAI_API_KEY.

