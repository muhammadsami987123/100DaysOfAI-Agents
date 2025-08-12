@echo off
echo ========================================
echo JobApplicationAgent - Installation Script
echo ========================================
echo.

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo To start the application:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run the server: python server.py
echo 3. Open your browser to: http://localhost:8012
echo.
echo Don't forget to create a .env file with your OpenAI API key!
echo.
pause
