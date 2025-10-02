@echo off
echo 🌍 Location Info Agent - Installation Script
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
    echo OPENAI_API_KEY=your_openai_api_key_here > .env
    echo GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here >> .env
    echo IMAGE_SEARCH_API_KEY=your_image_search_api_key_here >> .env
    echo TTS_ENGINE=openai >> .env
    echo.
    echo 📝 Please edit the .env file and add your API keys
    echo.
)

REM Test installation
echo.
echo 🧪 Testing installation...
python test_installation.py

echo.
echo 🎉 Installation completed!
echo.
echo 📋 Next steps:
echo 1. Edit .env file and add your API keys
echo 2. Run: python main.py
echo 3. Open: http://localhost:8000
echo.
echo 💡 Or use: start.bat to run the application
echo.
pause
