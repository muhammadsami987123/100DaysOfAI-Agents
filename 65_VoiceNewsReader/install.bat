@echo off
echo 🗞️ VoiceNewsReader - Installation Script
echo ================================

python --version >nul 2>&1
if errorlevel 1 (
  echo ❌ Python not found. Install Python 3.8+ from https://python.org
  pause
  exit /b 1
)

echo ✅ Python found
python --version

if exist "venv" (
  echo Removing existing virtual environment...
  rmdir /s /q venv
)

echo Creating virtual environment...
python -m venv venv || ( echo ❌ Failed to create venv & pause & exit /b 1 )

call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt || ( echo ❌ Failed to install deps & pause & exit /b 1 )

if not exist ".env" (
  echo Creating .env template...
  echo NEWSAPI_KEY=your_newsapi_key_here> .env
  echo BING_NEWS_KEY=your_bing_news_key_here>> .env
  echo GEMINI_API_KEY=your_gemini_api_key_here>> .env
  echo TTS_ENGINE=gemini>> .env
  echo DEBUG=True>> .env
)

echo 🧪 Verifying import...
python -c "import fastapi, requests, jinja2; print('OK')" || ( echo ❌ Import check failed & pause & exit /b 1 )

echo ✅ Installation complete. Run start.bat to launch.
pause


