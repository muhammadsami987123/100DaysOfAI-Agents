@echo off
echo Testing WhatsApp Scheduler Agent...
echo.

echo Running installation test...
python test_installation.py

echo.
echo Running demo...
python demo.py

echo.
echo Running examples...
python example_usage.py

echo.
echo Tests completed!
pause
