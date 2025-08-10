@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
cd /d %~dp0
echo Installing requirements...
pip install -r requirements.txt
echo Done.


