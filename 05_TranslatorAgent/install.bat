@echo off
echo ========================================
echo    TranslatorAgent - Day 5 Installation
echo ========================================
echo.

echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo Error installing dependencies. Please check your Python installation.
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.

echo Testing installation...
python test_installation.py

if %errorlevel% neq 0 (
    echo.
    echo Some tests failed. Please check the errors above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo To start the TranslatorAgent:
echo   python main.py --web
echo   python main.py --terminal
echo   python main.py --quick "Hello world" --target es
echo.
echo Don't forget to set your OpenAI API key:
echo   set OPENAI_API_KEY=your_api_key_here
echo.
pause 