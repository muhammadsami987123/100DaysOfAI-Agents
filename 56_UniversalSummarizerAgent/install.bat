@echo off

REM Create a virtual environment
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Install additional dependencies for document parsing
pip install requests beautifulsoup4 python-docx PyPDF2

echo Installation complete. You can now run the application using start.bat
pause
