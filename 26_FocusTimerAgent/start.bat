@echo off
setlocal
cd /d %~dp0
echo FocusTimerAgent - Pomodoro Assistant
echo.
REM Prefer repository root venv if available
set ROOT_VENV=..\venv\Scripts\activate.bat
set LOCAL_VENV=venv\Scripts\activate.bat

if exist "%ROOT_VENV%" (
    echo Using root venv: %ROOT_VENV%
    call %ROOT_VENV%
) else if exist "%LOCAL_VENV%" (
    call %LOCAL_VENV%
) else (
    echo No virtual environment found. Run install.bat first.
    pause
    exit /b 1
)
echo Choose an option:
echo 1. Start GUI
echo 2. Start CLI timer (defaults)
echo 3. Status
echo 4. Pause
echo 5. Resume
echo 6. Stop
echo 7. History
echo 8. Mute
echo 9. Unmute
set /p choice="Enter choice (1-9): "
if "%choice%"=="1" (
    python -m 26_FocusTimerAgent.gui_app
) else if "%choice%"=="2" (
    python -m 26_FocusTimerAgent.main start
) else if "%choice%"=="3" (
    python -m 26_FocusTimerAgent.main status
) else if "%choice%"=="4" (
    python -m 26_FocusTimerAgent.main pause
) else if "%choice%"=="5" (
    python -m 26_FocusTimerAgent.main resume
) else if "%choice%"=="6" (
    python -m 26_FocusTimerAgent.main stop
) else if "%choice%"=="7" (
    python -m 26_FocusTimerAgent.main history
) else if "%choice%"=="8" (
    python -m 26_FocusTimerAgent.main mute
) else if "%choice%"=="9" (
    python -m 26_FocusTimerAgent.main unmute
) else (
    echo Invalid choice.
)
endlocal


