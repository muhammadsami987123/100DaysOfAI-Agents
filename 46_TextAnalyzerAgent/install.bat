@echo off
echo Setting up virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Installing Node.js dependencies for Tailwind CSS...
npm install

echo Building Tailwind CSS...
npm run build

echo Installation complete.
pause
