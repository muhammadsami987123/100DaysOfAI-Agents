@echo off
echo Installing CryptoInsightsAgent...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install requirements
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    echo # CryptoInsightsAgent Configuration > .env
    echo # Get your OpenAI API key from https://platform.openai.com/api-keys >> .env
    echo OPENAI_API_KEY=your_openai_api_key_here >> .env
    echo. >> .env
    echo # Optional: CoinGecko API key for higher rate limits >> .env
    echo # Get it from https://www.coingecko.com/en/api >> .env
    echo COINGECKO_API_KEY= >> .env
    echo. >> .env
    echo # Default settings >> .env
    echo DEFAULT_CURRENCY=usd >> .env
    echo OPENAI_MODEL=gpt-4o-mini >> .env
    echo.
    echo .env file created! Please edit it with your API keys.
)

echo.
echo Installation completed successfully!
echo.
echo To run the agent:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Run the agent: python main.py
echo.
echo Or use the start.bat script for convenience.
echo.
pause
