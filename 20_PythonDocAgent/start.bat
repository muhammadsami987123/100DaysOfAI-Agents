@echo off
if not exist venv\Scripts\activate.bat (
	echo Virtual environment not found. Run install.bat first.
	pause > nul
	exit /b 1
)
call venv\Scripts\activate
python main.py %*
pause > nul
