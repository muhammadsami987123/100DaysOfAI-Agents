@echo off
echo ========================================
echo MindMapDiagramAgent - Starting Server
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting MindMapDiagramAgent server...
echo.
echo Server will be available at: http://127.0.0.1:8030
echo Press Ctrl+C to stop the server
echo.

python server.py

echo.
echo Server stopped.
pause
