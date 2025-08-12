@echo off
echo ========================================
echo JobApplicationAgent - Starting Server
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate

echo Starting JobApplicationAgent server...
echo.
echo Server will be available at: http://localhost:8012
echo Press Ctrl+C to stop the server
echo.

python server.py

pause
