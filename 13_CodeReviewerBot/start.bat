@echo off
echo ========================================
echo CodeReviewerBot - Day 13 Startup
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate

echo Starting CodeReviewerBot server...
echo.
echo Server will be available at: http://localhost:8013
echo Press Ctrl+C to stop the server
echo.

python server.py

echo.
echo Server stopped. Press any key to exit...
pause > nul
