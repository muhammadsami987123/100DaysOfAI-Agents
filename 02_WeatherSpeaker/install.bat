@echo off
echo 🌤️ Weather Speaker Agent - Installation Script
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

REM Install dependencies with specific versions to avoid conflicts
echo.
echo 📦 Installing dependencies...
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install openai==1.3.7
pip install requests==2.31.0
pip install python-multipart==0.0.6
pip install pyttsx3==2.90
pip install gTTS==2.4.0
pip install python-dotenv==1.0.0
pip install aiofiles==23.2.1
pip install jinja2==3.1.2
pip install httpx==0.25.2

echo.
echo ✅ Dependencies installed

REM Check for .env file
echo.
if not exist ".env" (
    echo ⚠️  No .env file found!
    echo Creating .env file template...
    echo OPENAI_API_KEY=your_openai_api_key_here > .env
    echo.
    echo 📝 Please edit the .env file and add your OpenAI API key
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
echo 1. Edit .env file and add your OpenAI API key
echo 2. Run: python main.py
echo 3. Open: http://localhost:8000
echo.
echo 💡 Or use: start.bat to run the application
echo.
pause 