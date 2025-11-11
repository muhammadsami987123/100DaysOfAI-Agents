
@echo off
echo "Setting up OfflineGPTJarvis..."

REM Create a virtual environment
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Install the required packages
pip install -r requirements.txt

echo "Setup complete. You can now run Jarvis by running 'python offline_jarvis.py'"
pause
