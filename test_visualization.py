#!/usr/bin/env python3
"""
Test script to verify the visualization works properly.
"""

import sys
import os

print("[TEST] Testing visualization script...")

try:
    # Try to import the module
    import visualize_owner_earnings
    print("[OK] Successfully imported visualize_owner_earnings")
    
    # Check if CSV files exist
    if os.path.exists('owner_earnings_financials_annual.csv'):
        print("[OK] Annual CSV file exists")
    else:
        print("[ERROR] Annual CSV file missing")
        
    if os.path.exists('owner_earnings_financials_quarterly.csv'):
        print("[OK] Quarterly CSV file exists")
    else:
        print("[ERROR] Quarterly CSV file missing")
    
    # Try to run the load_data function
    print("[TEST] Testing data loading...")
    annual_df, quarterly_df = visualize_owner_earnings.load_data()
    
    if annual_df is not None and quarterly_df is not None:
        print("[OK] Data loaded successfully")
        print(f"[INFO] Annual data: {len(annual_df)} rows")
        print(f"[INFO] Quarterly data: {len(quarterly_df)} rows")
    else:
        print("[ERROR] Failed to load data")
        
except Exception as e:
    print(f"[ERROR] Test failed: {e}")
    import traceback
    traceback.print_exc()

print("[TEST] Test completed")
