@echo off
setlocal
cd /d %~dp0
REM Prefer repository root venv if available
set ROOT_VENV=..\venv\Scripts\activate.bat
set LOCAL_VENV=venv\Scripts\activate.bat

if exist "%ROOT_VENV%" (
    echo Using root venv: %ROOT_VENV%
    call %ROOT_VENV%
) else if exist "%LOCAL_VENV%" (
    echo Using local venv: %LOCAL_VENV%
    call %LOCAL_VENV%
) else (
    echo No virtual environment found. Run install.bat first.
    pause
    exit /b 1
)
pip install pyinstaller
echo Building executable...
pyinstaller --noconfirm --onefile --windowed --name FocusTimerAgent ^
  --hidden-import pyttsx3.drivers ^
  --hidden-import pyttsx3.drivers.sapi5 ^
  --hidden-import win32com.client ^
  --hidden-import win32com.server ^
  --add-data "config.py;." ^
  --add-data "tts_service.py;." ^
  gui_app.py
if %errorlevel% neq 0 (
    echo PyInstaller failed.
    pause
    exit /b 1
)
echo Copying README next to the exe...
copy /Y README.md dist\ >nul
echo Build complete. Opening dist folder...
start "" explorer.exe "%cd%\dist"
echo Done. If the app doesn't start, run from terminal to see errors.
pause
endlocal


