@echo off
echo ========================================
echo TextFixer Assistant - Day 21 Startup
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate

echo Starting TextFixer Assistant (background hotkey listener)...
echo.
echo Default hotkey: Ctrl+.  ^|  Undo: Ctrl+Shift+W
echo Close this window or press Ctrl+C to stop.
echo.

python main.py

echo.
echo Assistant stopped. Press any key to exit...
pause > nul

