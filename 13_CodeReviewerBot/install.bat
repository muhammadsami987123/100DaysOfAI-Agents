@echo off
echo ========================================
echo CodeReviewerBot - Day 13 Installation
echo ========================================
echo.

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Create a .env file with your OpenAI API key
echo 2. Run: python server.py
echo 3. Open: http://localhost:8013
echo.
echo Press any key to exit...
pause > nul
