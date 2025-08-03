@echo off
echo Starting MarketSwimmer GUI with Logging...
echo.

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

REM Check for existing processes
tasklist /FI "WINDOWTITLE eq MarketSwimmer*" 2>NUL | find /I "python.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo WARNING: MarketSwimmer GUI may already be running!
    echo Check logs to identify multiple instances.
    echo.
)

echo Logs will be saved to: logs\
echo Current time: %date% %time%
echo PID will be logged for tracking multiple instances.
echo.

powershell -Command "& 'C:/Users/jerem/AppData/Local/Programs/Python/Python312/python.exe' market_swimmer_gui.py"
pause
