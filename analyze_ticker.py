"""
Complete workflow to analyze any ticker's owner earnings.
Usage: python analyze_ticker.py TICKER_SYMBOL
Example: python analyze_ticker.py BRK.B
"""

import sys
import os
import time
import subprocess
import webbrowser
from pathlib import Path

def clean_ticker_for_filename(ticker):
    """Clean ticker symbol for use in filenames."""
    return ticker.replace('.', '_').upper()

def open_stockrow_download(ticker):
    """Open StockRow download page for the specified ticker."""
    base_url = "https://stockrow.com/vector/exports/financials/{}?direction=desc"
    url = base_url.format(ticker.upper())
    
    print(f"[WEB] Opening StockRow download for {ticker.upper()}")
    print(f"[INFO] URL: {url}")
    print("\n[DOWNLOAD] Please download the XLSX file manually from your browser")
    print("[WAIT] The download monitor will detect it automatically...")
    
    webbrowser.open(url)
    return url

def run_download_monitor():
    """Run the download monitor to automatically copy files."""
    print("\n[DOWNLOAD] Starting download monitor...")
    print("[TIP] This will monitor your Downloads folder for new XLSX files")
    
    try:
        # Run the monitor with --check flag for one-time check
        result = subprocess.run([
            sys.executable, "monitor_downloads.py", "--check"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("[OK] Download monitor completed")
            print(result.stdout)
        else:
            print("[WARNING] Download monitor had issues:")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("[TIMEOUT] Download monitor timed out - continuing...")
    except Exception as e:
        print(f"[ERROR] Error running download monitor: {e}")

def run_owner_earnings_analysis():
    """Run the owner earnings analysis on the most recent XLSX file."""
    print("\n[ANALYSIS] Running Owner Earnings Analysis...")
    
    try:
        result = subprocess.run([
            sys.executable, "owner_earnings.py"
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("[OK] Owner earnings analysis completed")
            print(result.stdout)
            return True
        else:
            print("[ERROR] Owner earnings analysis failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("[TIMEOUT] Owner earnings analysis timed out")
        return False
    except Exception as e:
        print(f"[ERROR] Error running owner earnings analysis: {e}")
        return False

def run_visualization():
    """Generate the charts for the analysis."""
    print("\n[CHARTS] Generating visualizations...")
    
    try:
        # Use the correct Python executable path
        python_exe = r"C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe"
        
        result = subprocess.run([
            python_exe, "visualize_owner_earnings.py"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("[OK] Visualizations generated successfully")
            print(result.stdout)
            return True
        else:
            print("[ERROR] Visualization generation failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("[TIMEOUT] Visualization generation timed out")
        return False
    except Exception as e:
        print(f"[ERROR] Error generating visualizations: {e}")
        return False

def open_results():
    """Open the generated charts."""
    print("\n[CHARTS] Opening generated charts...")
    
    try:
        result = subprocess.run([
            sys.executable, "open_charts.py"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("[OK] Charts opened successfully")
            print(result.stdout)
        else:
            print("[WARNING] Issue opening charts:")
            print(result.stderr)
            
    except Exception as e:
        print(f"[ERROR] Error opening charts: {e}")

def check_prerequisites():
    """Check if all required files exist."""
    required_files = [
        "monitor_downloads.py",
        "owner_earnings.py", 
        "visualize_owner_earnings.py",
        "open_charts.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("[ERROR] Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True

def main():
    """Main function to run the complete ticker analysis workflow."""
    if len(sys.argv) != 2:
        print("Complete Ticker Analysis Workflow")
        print("=" * 40)
        print("\n[ERROR] Usage: python analyze_ticker.py TICKER_SYMBOL")
        print("\n[EXAMPLES]")
        print("   python analyze_ticker.py BRK.B")
        print("   python analyze_ticker.py AAPL")
        print("   python analyze_ticker.py TSLA")
        print("   python analyze_ticker.py AMZN")
        return
    
    ticker = sys.argv[1].upper()
    clean_ticker = clean_ticker_for_filename(ticker)
    
    print("Complete Ticker Analysis Workflow")
    print("=" * 40)
    print(f"[TARGET] Ticker: {ticker}")
    print(f"[CLEANED] Ticker: {clean_ticker}")
    
    # Check prerequisites
    print("\n[CHECK] Checking prerequisites...")
    if not check_prerequisites():
        return
    print("[OK] All required files found")
    
    # Step 1: Open StockRow download page
    print(f"\n{'='*50}")
    print("STEP 1: DOWNLOAD FINANCIAL DATA")
    print(f"{'='*50}")
    open_stockrow_download(ticker)
    
    # Wait for user to download
    input("\n[WAIT] Press Enter after you've downloaded the XLSX file...")
    
    # Step 2: Monitor downloads
    print(f"\n{'='*50}")
    print("STEP 2: COPY DOWNLOADED FILE")
    print(f"{'='*50}")
    run_download_monitor()
    
    # Step 3: Run owner earnings analysis
    print(f"\n{'='*50}")
    print("STEP 3: ANALYZE OWNER EARNINGS")
    print(f"{'='*50}")
    analysis_success = run_owner_earnings_analysis()
    
    if not analysis_success:
        print("[ERROR] Analysis failed. Please check if the XLSX file was downloaded correctly.")
        return
    
    # Step 4: Generate visualizations
    print(f"\n{'='*50}")
    print("STEP 4: GENERATE CHARTS")
    print(f"{'='*50}")
    viz_success = run_visualization()
    
    if not viz_success:
        print("[WARNING] Visualization failed, but analysis data should be available in CSV files.")
    
    # Step 5: Open results
    print(f"\n{'='*50}")
    print("STEP 5: VIEW RESULTS")
    print(f"{'='*50}")
    open_results()
    
    # Final summary
    print(f"\n{'='*50}")
    print("[SUCCESS] WORKFLOW COMPLETE!")
    print(f"{'='*50}")
    print(f"[TICKER] Analyzed: {ticker}")
    print("[FILES] Generated files:")
    print(f"   - owner_earnings_financials_annual.csv")
    print(f"   - owner_earnings_financials_quarterly.csv") 
    
    if viz_success:
        print("[CHARTS] Generated charts:")
        print(f"   - {clean_ticker.lower()}_owner_earnings_comparison.png")
        print(f"   - {clean_ticker.lower()}_earnings_components_breakdown.png")
        print(f"   - {clean_ticker.lower()}_volatility_analysis.png")
    
    print(f"\n[INFO] To analyze another ticker, run:")
    print(f"   python analyze_ticker.py [TICKER_SYMBOL]")

if __name__ == "__main__":
    main()
