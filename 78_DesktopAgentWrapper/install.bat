@echo off
echo 🖥️ DesktopAgentWrapper - Installation Script
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Create virtual environment
echo.
echo 🔧 Creating virtual environment...
if exist "venv" (
    echo Removing existing virtual environment...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment created

REM Activate virtual environment
echo.
echo 🔄 Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo.
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo 📦 Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo ✅ Dependencies installed

REM Check for .env file
echo.
if not exist ".env" (
    echo ⚠️  No .env file found!
    echo Creating .env file template...
    copy env.example .env
    echo.
    echo 📝 Please edit the .env file and add your API keys
    echo.
)

REM Create required directories
echo.
echo 📁 Creating required directories...
if not exist "assets" mkdir assets
if not exist "agents" mkdir agents
if not exist "sessions" mkdir sessions
if not exist "logs" mkdir logs
if not exist "exports" mkdir exports

echo ✅ Directories created

REM Test installation
echo.
echo 🧪 Testing installation...
python -c "import customtkinter; print('✅ CustomTkinter imported successfully')"
python -c "import desktop_gui; print('✅ DesktopAgentWrapper imported successfully')"

echo.
echo 🎉 Installation completed!
echo.
echo 📋 Next steps:
echo 1. Edit .env file and add your API keys
echo 2. Run: python main.py
echo 3. Select an agent from the dialog
echo.
echo 💡 Or use: start.bat to run the application
echo.
pause
