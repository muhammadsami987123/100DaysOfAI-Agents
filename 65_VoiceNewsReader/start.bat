@echo off
echo 🗞️ VoiceNewsReader - Starting...

if not exist "venv" (
  python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt

if not exist ".env" (
  echo ❌ .env not found. Please create it with NEWSAPI_KEY or BING_NEWS_KEY and GEMINI_API_KEY.
  pause
  exit /b 1
)

echo 🚀 Starting server at http://localhost:8000
python main.py
pause


