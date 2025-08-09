@echo off
cd /d %~dp0
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
echo Setup complete. Edit .env with your OpenAI key.
