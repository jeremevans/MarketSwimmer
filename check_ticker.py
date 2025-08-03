#!/usr/bin/env python3
"""
Check which ticker will be processed based on available XLSX files
"""

import os
import glob
from pathlib import Path

def detect_ticker_symbol():
    """Detect ticker symbol from most recent XLSX filename."""
    download_dir = Path("./downloaded_files")
    if not download_dir.exists():
        print("❌ No downloaded_files directory found")
        return None
    
    # Find all XLSX files
    xlsx_files = list(download_dir.glob("*.xlsx"))
    if not xlsx_files:
        print("❌ No XLSX files found in downloaded_files/")
        return None
    
    # Sort by modification time to get the most recent
    xlsx_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    most_recent = xlsx_files[0]
    
    print(f"📁 Most recent XLSX file: {most_recent.name}")
    print(f"📅 Modified: {most_recent.stat().st_mtime}")
    
    # Extract ticker from filename
    filename = most_recent.stem.lower()
    if 'financials_export_' in filename:
        parts = filename.split('_')
        if len(parts) >= 3:
            ticker = parts[2].upper()
            print(f"🎯 Detected ticker: {ticker}")
            return ticker
    
    print("❌ Could not detect ticker from filename")
    return None

def main():
    print("MarketSwimmer Ticker Detection Check")
    print("=" * 40)
    
    ticker = detect_ticker_symbol()
    
    if ticker:
        print(f"\n✅ Next analysis will process: {ticker}")
        print(f"📊 Expected chart files:")
        clean_ticker = ticker.replace('.', '_').lower()
        print(f"   - {clean_ticker}_earnings_components_breakdown.png")
        print(f"   - {clean_ticker}_owner_earnings_comparison.png") 
        print(f"   - {clean_ticker}_volatility_analysis.png")
    else:
        print(f"\n❌ No ticker detected. Please download XLSX data first.")
        print(f"💡 Use 'Download & Monitor' or manually download from StockRow")

if __name__ == "__main__":
    main()
