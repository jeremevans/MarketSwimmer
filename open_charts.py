import webbrowser
import os
import sys
from pathlib import Path

def open_charts(ticker):
    """Open the generated charts for the specified ticker in the default image viewer."""
    
    # Convert ticker to lowercase for filename matching
    ticker_lower = ticker.lower()
    
    chart_files = [
        f"{ticker_lower}_owner_earnings_comparison.png",
        f"{ticker_lower}_earnings_components_breakdown.png", 
        f"{ticker_lower}_volatility_analysis.png"
    ]
    
    print(f"[CHARTS] Opening {ticker.upper()} Owner Earnings Charts...")
    print("=" * 50)
    
    charts_opened = 0
    for chart_file in chart_files:
        if os.path.exists(chart_file):
            chart_path = os.path.abspath(chart_file)
            print(f"[OPEN] Opening: {chart_file}")
            
            # Try to open the file in the default image viewer
            try:
                # Use the file:// protocol to open local files
                webbrowser.open(f"file:///{chart_path}")
                print(f"   [OK] Opened in default viewer")
                charts_opened += 1
            except Exception as e:
                print(f"   [ERROR] Error opening file: {e}")
                print(f"   [PATH] Manual path: {chart_path}")
        else:
            print(f"[ERROR] Chart not found: {chart_file}")
            # Check if file exists with different case
            if os.path.exists(chart_file.upper()) or os.path.exists(chart_file.title()):
                print(f"   [HINT] Similar file might exist with different case")
    
    print("=" * 50)
    print(f"[SUMMARY] Opened {charts_opened} of {len(chart_files)} charts for {ticker.upper()}")
    
    if charts_opened == 0:
        print(f"[HELP] Expected chart files:")
        for chart_file in chart_files:
            print(f"   - {chart_file}")
        print(f"[HELP] Current working directory: {os.getcwd()}")
        print(f"[HELP] Available PNG files:")
        png_files = [f for f in os.listdir('.') if f.endswith('.png')]
        for png_file in png_files:
            print(f"   - {png_file}")

    print(f"\n[FOLDER] All charts are saved in: {os.getcwd()}")
    print(f"\n[INFO] Chart descriptions for {ticker.upper()}:")
    print(f"• {ticker_lower}_owner_earnings_comparison.png - Annual and quarterly owner earnings trends")
    print(f"• {ticker_lower}_earnings_components_breakdown.png - Breakdown of earnings components")
    print(f"• {ticker_lower}_volatility_analysis.png - Volatility and distribution analysis")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python open_charts.py <TICKER>")
        print("Example: python open_charts.py ROOT")
        sys.exit(1)
    
    ticker = sys.argv[1]
    open_charts(ticker)
