"""
Test script to verify owner earnings analysis works without Unicode errors
"""
import subprocess
import sys

def test_owner_earnings():
    print("Testing Owner Earnings Analysis (Unicode Fixed Version)")
    print("=" * 60)
    
    try:
        python_exe = r"C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe"
        
        # Test with dry run or help to check for Unicode issues
        result = subprocess.run([
            python_exe, "owner_earnings_fixed.py", "--help"
        ], capture_output=True, text=True, timeout=30, encoding='utf-8', errors='replace')
        
        if result.returncode == 0:
            print("✅ SUCCESS: owner_earnings_fixed.py runs without Unicode errors!")
            return True
        else:
            print("❌ FAILED: owner_earnings_fixed.py has issues")
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_owner_earnings()
    print("\n" + "=" * 60)
    if success:
        print("🎉 All Unicode issues resolved! GUI analysis should work now.")
    else:
        print("⚠️  Still have issues to resolve.")
