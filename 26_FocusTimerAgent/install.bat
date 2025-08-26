@echo off
setlocal
cd /d %~dp0
REM Prefer repository root venv if available
set ROOT_VENV=..\venv\Scripts\activate.bat
set LOCAL_VENV=venv\Scripts\activate.bat

if exist "%ROOT_VENV%" (
    echo Using root venv: %ROOT_VENV%
    call %ROOT_VENV%
) else (
    if not exist "%LOCAL_VENV%" (
        echo Root venv not found. Creating local venv...
        python -m venv venv
        if %errorlevel% neq 0 (
            echo Error: Failed to create local virtual environment
            exit /b 1
        )
    )
    call %LOCAL_VENV%
)
python -m pip install --upgrade pip || exit /b 1
pip install -r requirements.txt || exit /b 1
echo Installation complete.
endlocal


