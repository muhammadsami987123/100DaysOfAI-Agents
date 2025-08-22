@echo off
setlocal
python -m pip install --upgrade pip || exit /b 1
pip install -r "%~dp0requirements.txt" || exit /b 1
echo Installation complete.
endlocal

