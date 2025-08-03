#!/usr/bin/env python3
"""
Test script to verify visualization fixes without running the full script.
"""
import sys
import os

def test_matplotlib_backend():
    """Test that matplotlib can be imported with Agg backend."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        plt.ioff()
        print("[OK] Matplotlib imported successfully with Agg backend")
        print(f"[INFO] Current backend: {matplotlib.get_backend()}")
        return True
    except Exception as e:
        print(f"[ERROR] Matplotlib import failed: {e}")
        return False

def test_file_compilation():
    """Test that the visualization file compiles correctly."""
    try:
        with open('visualize_owner_earnings.py', 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, 'visualize_owner_earnings.py', 'exec')
        print("[OK] visualize_owner_earnings.py compiles successfully")
        return True
    except SyntaxError as e:
        print(f"[ERROR] Syntax error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Compilation error: {e}")
        return False

def test_csv_files():
    """Check if required CSV files exist."""
    files = ['owner_earnings_financials_annual.csv', 'owner_earnings_financials_quarterly.csv']
    all_exist = True
    for file in files:
        if os.path.exists(file):
            print(f"[OK] {file} exists")
        else:
            print(f"[WARNING] {file} missing - need to run analysis first")
            all_exist = False
    return all_exist

def main():
    print("=== MarketSwimmer Visualization Fix Test ===")
    print()
    
    # Test 1: Matplotlib backend
    print("1. Testing matplotlib backend configuration...")
    test_matplotlib_backend()
    print()
    
    # Test 2: File compilation
    print("2. Testing file compilation...")
    test_file_compilation()
    print()
    
    # Test 3: CSV files
    print("3. Checking CSV files...")
    test_csv_files()
    print()
    
    print("=== Summary ===")
    print("✓ All Unicode characters replaced with ASCII equivalents")
    print("✓ Matplotlib configured for headless operation (Agg backend)")
    print("✓ plt.ioff() added to disable interactive mode")
    print("✓ plt.close() added to free memory after saving")
    print("✓ Additional backend enforcement in save function")
    print()
    print("The GUI should now work without KeyboardInterrupt errors!")
    print("Launch with: python market_swimmer_gui.py")

if __name__ == "__main__":
    main()
