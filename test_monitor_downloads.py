#!/usr/bin/env python3
"""
Simple test to check if monitor_downloads.py spawns GUI
"""
import subprocess
import sys

def test_monitor_downloads():
    print("Testing monitor_downloads.py without GUI spawning...")
    
    try:
        python_exe = r"C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe"
        result = subprocess.run([
            python_exe, "monitor_downloads.py", "--check"
        ], capture_output=True, text=True, timeout=10, encoding='utf-8', errors='replace')
        
        print("Return code:", result.returncode)
        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr)
        
        if "start_gui" in result.stdout.lower() or "start_gui" in result.stderr.lower():
            print("[ERROR] monitor_downloads.py is still trying to launch GUI!")
        else:
            print("[OK] monitor_downloads.py completed without launching GUI")
            
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")

if __name__ == "__main__":
    test_monitor_downloads()
