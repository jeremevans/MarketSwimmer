@echo off
REM Complete Ticker Analysis - Windows Batch File
REM Usage: analyze.bat TICKER_SYMBOL
REM Example: analyze.bat BRK.B

if "%1"=="" (
    echo.
    echo 📊 Complete Ticker Analysis Workflow
    echo =====================================
    echo.
    echo ❌ Usage: analyze.bat TICKER_SYMBOL
    echo.
    echo 📋 Examples:
    echo    analyze.bat BRK.B
    echo    analyze.bat AAPL
    echo    analyze.bat TSLA
    echo    analyze.bat AMZN
    echo.
    pause
    exit /b 1
)

echo.
echo 📊 Starting analysis for ticker: %1
echo.

python analyze_ticker.py %1

echo.
echo 🎉 Analysis complete! Check the generated files and charts.
echo.
pause
