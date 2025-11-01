@echo off
echo ####################################################################
echo #                                                                  #
echo #           VideoChapterAgent - One-Click Installer              #
echo #                                                                  #
echo ####################################################################

echo.
echo [1/7] Checking Python Installation...
python --version > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found. Please install Python 3.8+ from https://www.python.org/downloads/
    PAUSE
    EXIT /B 1
)
FOR /F "tokens=*" %%i IN ('python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') DO SET PYTHON_VERSION=%%i
IF "%PYTHON_VERSION:~0,3%" LSS "3.8" (
    echo ❌ Python version %PYTHON_VERSION% detected. Please install Python 3.8+
    PAUSE
    EXIT /B 1
)
echo ✅ Python %PYTHON_VERSION% is installed.

echo.
echo [2/7] Checking FFmpeg Installation...
ffmpeg -version > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ FFmpeg not found. Please install FFmpeg and add it to your system PATH.
    echo    Download from: https://ffmpeg.org/download.html
    PAUSE
    EXIT /B 1
)
echo ✅ FFmpeg is installed.

echo.
echo [3/7] Creating Virtual Environment...
python -m venv venv
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to create virtual environment.
    PAUSE
    EXIT /B 1
)
echo ✅ Virtual environment created.

echo.
echo [4/7] Activating Virtual Environment...
call venv\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to activate virtual environment.
    PAUSE
    EXIT /B 1
)
echo ✅ Virtual environment activated.

echo.
echo [5/7] Installing Dependencies...
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to install dependencies.
    PAUSE
    EXIT /B 1
)
echo ✅ All dependencies installed.

echo.
echo [6/7] Setting up Environment Variables (API Keys)...
IF NOT EXIST .env (
    echo GEMINI_API_KEY=your_gemini_api_key_here > .env
    echo OPENAI_API_KEY=your_openai_api_key_here >> .env
    echo 📝 Created .env file. Please edit it with your actual API keys.
) ELSE (
    echo ✅ .env file already exists. Skipping creation.
)

echo.
echo [7/7] Running Installation Tests...
python -m pytest test/
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Installation tests failed. Please check the output above for details.
    PAUSE
    EXIT /B 1
)
echo ✅ Installation tests passed.

echo.
echo ####################################################################
echo #                                                                  #
echo #           VideoChapterAgent - Installation Complete!           #
echo #                                                                  #
echo ####################################################################
echo.
echo To start the web application, run:
echo python main.py
echo.
echo Then open your browser to: http://localhost:8000
echo.
PAUSE
EXIT /B 0
