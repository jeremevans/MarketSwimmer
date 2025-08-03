"""
Non-interactive version of analyze_ticker.py for GUI use.
This automatically processes without user prompts.
"""

import sys
import os
import time
import subprocess
import webbrowser
from pathlib import Path

# Import logging system
from logger_config import get_logger, log_subprocess_call, log_function_entry, log_function_exit

# Initialize logger
logger = get_logger()

def clean_ticker_for_filename(ticker):
    """Clean ticker symbol for use in filenames."""
    return ticker.replace('.', '_').upper()

def run_owner_earnings_analysis(ticker):
    """Run the owner earnings analysis for the specified ticker."""
    print("\n[ANALYSIS] Running Owner Earnings Analysis...")
    
    try:
        python_exe = r"C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe"
        result = subprocess.run([
            python_exe, "owner_earnings_fixed.py", ticker
        ], capture_output=True, text=True, timeout=120, encoding='utf-8', errors='replace')
        
        print(f"[ANALYSIS] Return code: {result.returncode}")
        
        if result.returncode == 0:
            print("[OK] Owner Earnings Analysis completed")
            print(result.stdout)
        else:
            print("[ERROR] Owner Earnings Analysis failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("[TIMEOUT] Owner Earnings Analysis timed out")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to run Owner Earnings Analysis: {e}")
        return False
        
    return True

def open_stockrow_download(ticker):
    """Open StockRow download page for the specified ticker."""
    base_url = "https://stockrow.com/vector/exports/financials/{}?direction=desc"
    url = base_url.format(ticker.upper())
    
    print(f"[WEB] Opening StockRow download for {ticker.upper()}")
    print(f"[INFO] URL: {url}")
    print("\n[AUTO] Automatically opening browser...")
    
    webbrowser.open(url)
    return url

def run_download_monitor():
    """Run the download monitor to automatically copy files."""
    log_function_entry(logger, "run_download_monitor")
    print("\n[DOWNLOAD] Starting download monitor...")
    
    try:
        # Run the monitor with --check flag for one-time check
        python_exe = r"C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe"
        command = [python_exe, "monitor_downloads.py", "--check"]
        logger.info(f"Executing download monitor: {' '.join(command)}")
        log_subprocess_call(logger, ' '.join(command), "analyze_ticker_gui.py")
        
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=30, encoding='utf-8', errors='replace'
        )
        
        logger.info(f"Download monitor return code: {result.returncode}")
        if result.returncode == 0:
            print("[OK] Download monitor completed")
            print(result.stdout)
            logger.debug(f"Download monitor stdout: {result.stdout}")
        else:
            print("[WARNING] Download monitor had issues:")
            print(result.stderr)
            logger.warning(f"Download monitor stderr: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        logger.error("Download monitor timed out")
        print("[TIMEOUT] Download monitor timed out - continuing...")
    except Exception as e:
        logger.error(f"Error running download monitor: {e}")
        print(f"[ERROR] Error running download monitor: {e}")

    log_function_exit(logger, "run_download_monitor")

def run_visualization():
    """Generate the charts for the analysis."""
    print("\n[CHARTS] Generating visualizations...")
    
    try:
        python_exe = r"C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe"
        
        result = subprocess.run([
            python_exe, "visualize_owner_earnings.py"
        ], capture_output=True, text=True, timeout=60, encoding='utf-8', errors='replace')
        
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

def open_results(ticker):
    """Open the generated charts for the specified ticker."""
    print("\n[CHARTS] Opening generated charts...")
    
    try:
        python_exe = r"C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe"
        result = subprocess.run([
            python_exe, "open_charts.py", ticker
        ], capture_output=True, text=True, timeout=30, encoding='utf-8', errors='replace')
        
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
        "owner_earnings_fixed.py", 
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

def check_for_existing_data():
    """Check if XLSX files already exist in downloaded_files folder."""
    download_dir = Path("./downloaded_files")
    if download_dir.exists():
        xlsx_files = list(download_dir.glob("*.xlsx"))
        if xlsx_files:
            print(f"[FOUND] {len(xlsx_files)} existing XLSX file(s) in downloaded_files/")
            for xlsx_file in xlsx_files[-3:]:  # Show last 3 files
                print(f"   - {xlsx_file.name}")
            return True
    return False

def main():
    """Main function to run the complete ticker analysis workflow."""
    log_function_entry(logger, "analyze_ticker_gui.main", args=sys.argv)
    logger.info("="*60)
    logger.info("ANALYZE_TICKER_GUI STARTED")
    logger.info(f"Arguments: {sys.argv}")
    logger.info(f"PID: {os.getpid()}")
    logger.info("="*60)
    
    if len(sys.argv) != 2:
        logger.error("Invalid number of arguments provided")
        print("Complete Ticker Analysis Workflow (GUI Version)")
        print("=" * 50)
        print("\n[ERROR] Usage: python analyze_ticker_gui.py TICKER_SYMBOL")
        print("\n[EXAMPLES]")
        print("   python analyze_ticker_gui.py BRK.B")
        print("   python analyze_ticker_gui.py AAPL")
        print("   python analyze_ticker_gui.py TSLA")
        print("   python analyze_ticker_gui.py AMZN")
        return
    
    ticker = sys.argv[1].upper()
    clean_ticker = clean_ticker_for_filename(ticker)
    
    print("Complete Ticker Analysis Workflow (GUI Version)")
    print("=" * 50)
    print(f"[TARGET] Ticker: {ticker}")
    print(f"[CLEANED] Ticker: {clean_ticker}")
    
    # Check prerequisites
    print("\n[CHECK] Checking prerequisites...")
    if not check_prerequisites():
        return
    print("[OK] All required files found")
    
    # Check for existing data
    has_existing_data = check_for_existing_data()
    
    # Step 1: Open StockRow download page
    print(f"\n{'='*50}")
    print("STEP 1: DOWNLOAD FINANCIAL DATA")
    print(f"{'='*50}")
    open_stockrow_download(ticker)
    
    # Wait a bit for browser to open, then check downloads
    print("[INFO] Waiting 5 seconds for browser to open...")
    time.sleep(5)
    
    # Step 2: Monitor downloads
    print(f"\n{'='*50}")
    print("STEP 2: COPY DOWNLOADED FILE")
    print(f"{'='*50}")
    run_download_monitor()
    
    # Check again for data
    has_data_now = check_for_existing_data()
    
    if not has_data_now and not has_existing_data:
        print("[WARNING] No XLSX files found. You may need to download the file manually.")
        print("[INFO] Please download the XLSX file from the opened browser window.")
        print("[INFO] The analysis will continue with any existing data...")
    
    # Step 3: Run owner earnings analysis
    print(f"\n{'='*50}")
    print("STEP 3: ANALYZE OWNER EARNINGS")
    print(f"{'='*50}")
    analysis_success = run_owner_earnings_analysis(ticker)
    
    if not analysis_success:
        print("[ERROR] Analysis failed. Please check if XLSX files are available.")
        print("[INFO] You may need to manually download the data from StockRow.")
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
    open_results(clean_ticker)
    
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
    
    print(f"\n[INFO] Analysis complete for {ticker}")

if __name__ == "__main__":
    main()
