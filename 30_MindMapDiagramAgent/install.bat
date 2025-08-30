@echo off
echo ========================================
echo MindMapDiagramAgent - Installation
echo ========================================
echo.

echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    echo Please ensure Python is installed and in your PATH
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Creating necessary directories...
if not exist "uploads" mkdir uploads
if not exist "exports" mkdir exports
if not exist "temp" mkdir temp

echo.
echo Testing installation...
python test_installation.py
if %errorlevel% neq 0 (
    echo Warning: Some dependencies may not be properly installed
    echo You can run 'python test_installation.py' to check again
)

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Create a .env file with your OpenAI API key
echo 2. Run start.bat to start the application
echo 3. Open http://127.0.0.1:8030 in your browser
echo.
pause
