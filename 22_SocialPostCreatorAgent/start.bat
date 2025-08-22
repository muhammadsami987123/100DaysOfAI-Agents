@echo off
setlocal
echo SocialPostCreatorAgent - AI Social Media Post Generator
echo Features: Generate, Edit, Copy, Save Posts
echo Choose Interface:
echo.
echo 1. CLI Interface (Interactive)
echo 2. Web UI (Browser)
echo 3. CLI with specific parameters
echo 4. Setup/Install Dependencies
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Starting CLI interface...
    python -m 22_SocialPostCreatorAgent.cli
) else if "%choice%"=="2" (
    echo Starting Web UI...
    echo Open your browser to: http://localhost:5000
    python -m 22_SocialPostCreatorAgent.web_app
) else if "%choice%"=="3" (
    echo CLI with parameters...
    set /p platform="Platform (e.g., Twitter): "
    set /p topic="Topic (e.g., AI in Education): "
    set /p tone="Tone (e.g., professional): "
    python -m 22_SocialPostCreatorAgent.cli --platform "%platform%" --topic "%topic%" --tone "%tone%" --save --copy
) else if "%choice%"=="4" (
    echo Running setup...
    python setup.py
) else (
    echo Invalid choice. Starting CLI interface...
    python -m 22_SocialPostCreatorAgent.cli
)
endlocal

