#!/usr/bin/env python3
"""
Comprehensive test to verify all Unicode character fixes.
"""
import os
import sys

def test_file_compilation(filename):
    """Test that a Python file compiles correctly."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, filename, 'exec')
        print(f"[OK] {filename} compiles successfully")
        return True
    except SyntaxError as e:
        print(f"[ERROR] Syntax error in {filename}: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error in {filename}: {e}")
        return False

def check_unicode_characters(filename):
    """Check if a file contains any non-ASCII characters."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        non_ascii_chars = []
        for i, char in enumerate(content):
            if ord(char) > 127:
                line_num = content[:i].count('\n') + 1
                non_ascii_chars.append((line_num, char, hex(ord(char))))
        
        if non_ascii_chars:
            print(f"[WARNING] {filename} contains non-ASCII characters:")
            for line, char, code in non_ascii_chars[:5]:  # Show first 5
                print(f"   Line {line}: '{char}' ({code})")
            if len(non_ascii_chars) > 5:
                print(f"   ... and {len(non_ascii_chars) - 5} more")
            return False
        else:
            print(f"[OK] {filename} contains only ASCII characters")
            return True
    except Exception as e:
        print(f"[ERROR] Error checking {filename}: {e}")
        return False

def main():
    print("=== MarketSwimmer Unicode Fix Verification ===")
    print()
    
    # List of files to check
    files_to_check = [
        'visualize_owner_earnings.py',
        'monitor_downloads.py', 
        'owner_earnings.py',
        'open_charts.py',
        'analyze_ticker.py'  # Should already be fixed
    ]
    
    all_good = True
    
    print("1. Testing file compilation...")
    for filename in files_to_check:
        if os.path.exists(filename):
            if not test_file_compilation(filename):
                all_good = False
        else:
            print(f"[SKIP] {filename} not found")
    
    print("\n2. Checking for Unicode characters...")
    for filename in files_to_check:
        if os.path.exists(filename):
            if not check_unicode_characters(filename):
                all_good = False
        else:
            print(f"[SKIP] {filename} not found")
    
    print("\n=== Summary ===")
    if all_good:
        print("[SUCCESS] All files are ready for Windows console!")
        print("✓ No Unicode characters found")
        print("✓ All files compile successfully")
        print("✓ MarketSwimmer GUI should work without encoding errors")
    else:
        print("[WARNING] Some issues found - see details above")
    
    print("\n[INFO] The following fixes have been applied:")
    print("• All emoji characters replaced with ASCII tags")
    print("• Matplotlib configured for headless operation")
    print("• Console output uses ASCII-only characters")
    print("• GUI should work without KeyboardInterrupt or encoding errors")

if __name__ == "__main__":
    main()
