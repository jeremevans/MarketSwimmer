@echo off
echo Testing MarketSwimmer GUI without logging...
echo.

REM First try with the full Python path
echo Attempting to start GUI...
"C:/Users/jerem/AppData/Local/Programs/Python/Python312/python.exe" market_swimmer_gui.py

echo.
echo If no window appeared, there may be an issue with the GUI.
pause
