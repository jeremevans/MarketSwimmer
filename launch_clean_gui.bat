@echo off
echo Starting MarketSwimmer GUI (Clean Version)...
cd /d "C:\Users\jerem\local\MarketSwimmer"
"C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe" market_swimmer_gui_clean.py
if errorlevel 1 (
    echo.
    echo Error occurred while starting GUI
    pause
)
