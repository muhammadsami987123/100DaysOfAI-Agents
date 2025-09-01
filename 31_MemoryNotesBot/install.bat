@echo off
echo ========================================
echo MemoryNotesBot Installation Script
echo ========================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install dependencies
    echo Please make sure Python and pip are installed
    pause
    exit /b 1
)

echo.
echo Creating necessary directories...
if not exist "data" mkdir data
if not exist "data\exports" mkdir data\exports

echo.
echo Copying environment file...
if not exist ".env" (
    copy "env.example" ".env"
    echo Please edit .env file and add your OpenAI API key
) else (
    echo .env file already exists
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To get started:
echo 1. Edit .env file and add your OpenAI API key
echo 2. Run: python main.py --demo (to add sample data)
echo 3. Run: python main.py --cli (for command line interface)
echo 4. Run: python main.py --web (for web interface)
echo.
echo For help: python main.py --help
echo.
pause
