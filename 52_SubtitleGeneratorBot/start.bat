@echo off
setlocal ENABLEDELAYEDEXPANSION

cd /d %~dp0

if not exist venv (
	call install.bat
)
call venv\Scripts\activate

set HOST=%HOST:="=%
set PORT=%PORT:="=%

python main.py
