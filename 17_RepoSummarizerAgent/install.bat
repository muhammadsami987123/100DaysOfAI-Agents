@echo off
echo ========================================
echo RepoSummarizerAgent - Day 17 Installation
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
echo 2. Run: python main.py --url https://github.com/user/repo
echo.
echo Example usage:
echo   python main.py --url https://github.com/user/repo --lang hi
echo   python main.py --url https://github.com/user/repo --lang ur --save
echo.
echo Press any key to exit...
pause > nul
