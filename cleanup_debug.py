#!/usr/bin/env python3
"""
Script to clean up debug statements from charts.py
"""

import re

def cleanup_debug_statements():
    """Remove debug print statements from charts.py"""
    
    # Read the file
    with open('marketswimmer/visualization/charts.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_lines = len(content.splitlines())
    
    # Remove debug print statements - more comprehensive patterns
    patterns_to_remove = [
        r'\s*print\(f"\[DEBUG\].*?"\)\n',
        r'\s*print\(f\"\[DEBUG\].*?\"\)\n',
        r"    print\(f'\[DEBUG\].*?'\)\n",
        r'        print\(f"\[DEBUG\].*?"\)\n',
        r'            print\(f"\[DEBUG\].*?"\)\n',
    ]
    
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Clean up any empty lines that might be left behind (more than 2 consecutive)
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # Write back to file
    with open('marketswimmer/visualization/charts.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    new_lines = len(content.splitlines())
    print(f'Cleanup complete: {original_lines} -> {new_lines} lines ({original_lines - new_lines} lines removed)')

if __name__ == "__main__":
    cleanup_debug_statements()
