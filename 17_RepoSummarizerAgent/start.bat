@echo off
echo ========================================
echo RepoSummarizerAgent - Day 17
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo RepoSummarizerAgent is ready!
echo.
echo Usage examples:
echo   python main.py --url https://github.com/user/repo
echo   python main.py --url https://github.com/user/repo --lang hi
echo   python main.py --url https://github.com/user/repo --lang ur --save
echo.
echo For help: python main.py --help
echo.
echo Press any key to exit...
pause > nul
