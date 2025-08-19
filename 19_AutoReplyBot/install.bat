@echo off
setlocal
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
echo Installation complete. Set OPENAI_API_KEY in a .env file or environment.
endlocal

