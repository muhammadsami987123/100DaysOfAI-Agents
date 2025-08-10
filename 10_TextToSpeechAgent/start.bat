@echo off
cd /d %~dp0
if not exist .env (
  echo OPENAI_API_KEY=>>.env
  echo TTS_ENGINE=openai>>.env
  echo PORT=8009>>.env
)
for /f "tokens=*" %%i in ('type .env ^| findstr /r "^PORT="') do set %%i
if "%PORT%"=="" set PORT=8009
echo Starting server on port %PORT% ...
uvicorn server:app --host 0.0.0.0 --port %PORT%


