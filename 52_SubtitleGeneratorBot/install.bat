@echo off
setlocal ENABLEDELAYEDEXPANSION

cd /d %~dp0

if not exist venv (
	python -m venv venv
)
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

if not exist .env (
	echo OPENAI_API_KEY= >> .env
	echo OPENAI_MODEL=gpt-4o-mini >> .env
	echo HOST=127.0.0.1 >> .env
	echo PORT=8022 >> .env
	echo DEBUG=true >> .env
	echo Created .env template. Please fill in OPENAI_API_KEY.
)

echo Installation complete. Edit .env and run start.bat
