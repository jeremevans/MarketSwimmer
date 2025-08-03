@echo off
echo ===============================================
echo MarketSwimmer GUI Launcher (Safe Start)  
echo ===============================================

echo Checking for existing GUI processes...

REM Check if MarketSwimmer GUI is already running
tasklist /FI "WINDOWTITLE eq MarketSwimmer*" 2>NUL | find /I "python.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo MarketSwimmer GUI is already running!
    echo Please close existing windows before starting a new one.
    pause
    exit /b 1
)

echo No existing GUI found. Starting clean version...
echo.

cd /d "C:\Users\jerem\local\MarketSwimmer"

echo Current directory: %CD%
echo Python executable: C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe
echo.

echo Starting MarketSwimmer GUI (Clean Version)...
"C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe" market_swimmer_gui_clean.py

if errorlevel 1 (
    echo.
    echo Error occurred while starting GUI
    echo Check that all dependencies are installed
    pause
) else (
    echo.
    echo GUI closed normally.
)
