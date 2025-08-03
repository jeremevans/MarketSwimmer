"""
Fix Unicode/emoji issues in owner_earnings.py for Windows command prompt compatibility.
This script will replace all emoji characters with ASCII-compatible alternatives.
"""

import re

def fix_unicode_issues():
    """Replace emoji characters with ASCII alternatives in owner_earnings.py."""
    
    # Read the current file
    with open('owner_earnings.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define emoji replacements
    replacements = {
        '📊': '[DATA]',
        '✅': '[OK]',
        '❌': '[ERROR]',
        '💡': '[TIP]',
        '📁': '[FILE]',
        '💾': '[SAVE]',
        '🎯': '[TARGET]',
        '📈': '[CHART]',
        '🔍': '[SEARCH]',
        '⚠️': '[WARNING]',
        '📋': '[INFO]',
        '💰': '[MONEY]',
        '🏭': '[COMPANY]',
        '📉': '[DECLINE]',
        '�': '[DATE]',
        '💳': '[CREDIT]',
        # Unicode escape sequences
        '\\U0001f4c1': '[FILE]',
        '\\U0001f4ca': '[DATA]',
        '\\U00002705': '[OK]',
        '\\U0000274c': '[ERROR]',
        '\\U0001f4a1': '[TIP]',
        '\\U0001f4be': '[SAVE]',
    }
    
    # Apply replacements
    for emoji, replacement in replacements.items():
        content = content.replace(emoji, replacement)
    
    # Write the fixed content back
    with open('owner_earnings_fixed.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed file created: owner_earnings_fixed.py")
    print("Emoji characters replaced with ASCII alternatives:")
    for emoji, replacement in replacements.items():
        if emoji in content:
            print(f"  {emoji} -> {replacement}")

if __name__ == "__main__":
    fix_unicode_issues()
