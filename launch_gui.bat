@echo off
echo Starting MarketSwimmer GUI...
echo.
echo Please wait while the GUI loads...
echo.

REM Try different Python executable paths
if exist "C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe" (
    echo Using Python 3.12...
    "C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe" market_swimmer_gui.py
) else if exist "python.exe" (
    echo Using system Python...
    python market_swimmer_gui.py
) else if exist "python3.exe" (
    echo Using python3...
    python3 market_swimmer_gui.py
) else (
    echo ERROR: Python executable not found!
    echo Please make sure Python is installed and accessible.
    echo.
    echo Trying 'py' command as fallback...
    py market_swimmer_gui.py
)

echo.
echo GUI has closed.
pause
