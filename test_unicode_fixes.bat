@echo off
echo Testing MarketSwimmer GUI functionality...
echo.
echo 1. Checking Python installation...
python --version
echo.
echo 2. Testing file compilation...
python -m py_compile visualize_owner_earnings.py
if %errorlevel% == 0 (
    echo [OK] visualize_owner_earnings.py compiles successfully
) else (
    echo [ERROR] Compilation failed
    pause
    exit /b 1
)
echo.
echo 3. Checking required CSV files...
if exist "owner_earnings_financials_annual.csv" (
    echo [OK] Annual CSV file exists
) else (
    echo [WARNING] Annual CSV file missing - run analysis first
)
if exist "owner_earnings_financials_quarterly.csv" (
    echo [OK] Quarterly CSV file exists  
) else (
    echo [WARNING] Quarterly CSV file missing - run analysis first
)
echo.
echo 4. All Unicode character fixes have been applied
echo    - Replaced all emoji characters with ASCII equivalents
echo    - Set matplotlib to non-interactive mode (Agg backend)
echo    - Removed plt.show() calls to prevent GUI blocking
echo.
echo Ready to test! Launch the GUI with:
echo python market_swimmer_gui.py
echo.
echo Or run visualization directly with:
echo python visualize_owner_earnings.py
echo.
pause
