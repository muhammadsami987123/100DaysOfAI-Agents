@echo off
cd /d %~dp0
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
if not exist ".env" (
  echo OPENAI_API_KEY=your_openai_api_key_here> .env
  echo SLIDES_MODEL=gpt-4o-mini>> .env
  echo PORT=8080>> .env
  echo SLIDES_MIN=20>> .env
  echo SLIDES_MAX=22>> .env
  echo INCLUDE_IMAGES=true>> .env
  echo DOWNLOAD_IMAGES=false>> .env
  echo IMAGE_TIMEOUT_SEC=10>> .env
)
echo Installation complete.
pause


