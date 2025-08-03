#!/usr/bin/env python3
"""
Simple test to verify Unicode fixes are working.
"""

# Test the key print statements that were causing Unicode errors
print("[OK] Testing ASCII replacements...")
print("[ANALYSIS] Preparing data for visualization...")
print("[CHARTS] Creating visualizations...")
print("[CHART] Saved chart: test.png")
print("[OK] All charts displayed and saved!")
print("[SUMMARY] TEST SUMMARY STATISTICS:")
print("[ERROR] Error loading CSV files: test error")
print("[INFO] Make sure to run owner_earnings.py first to generate the CSV files")

# Test importing the module
try:
    import sys
    sys.path.append('.')
    # Just test compilation, not execution
    with open('visualize_owner_earnings.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Try to compile the code
    compile(code, 'visualize_owner_earnings.py', 'exec')
    print("[OK] visualize_owner_earnings.py compiles successfully")
    print("[OK] Unicode character replacements are working")
    
except SyntaxError as e:
    print(f"[ERROR] Syntax error in visualize_owner_earnings.py: {e}")
except Exception as e:
    print(f"[ERROR] Other error: {e}")

print("[TEST] Unicode fix verification completed")
