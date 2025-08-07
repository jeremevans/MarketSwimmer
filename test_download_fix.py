#!/usr/bin/env python3
"""Test script for download detection fix"""

from marketswimmer.core.download_manager import DownloadManager
from pathlib import Path

# Create test files to simulate the scenario
Path('downloaded_files').mkdir(exist_ok=True)
zion_file = Path('downloaded_files/financials_export_zion_2025_08_07_134246.xlsx')
zion_file.touch()

# Test the download manager
dm = DownloadManager()

print('=== TESTING FIXED DOWNLOAD DETECTION LOGIC ===')
print()
print('Testing ZION file detection...')
print(f'ZION file exists: {zion_file.exists()}')
print(f'Is ZION file valid for ZION ticker? {dm._is_financial_data_file(zion_file, "ZION")}')
print(f'Is ZION file valid for NWN ticker? {dm._is_financial_data_file(zion_file, "NWN")}')

print()
print('Testing file pattern matching...')
print(f'ZION file: {zion_file.name}')
print(f'Contains "financials_export_zion": {"financials_export_zion" in zion_file.name.lower()}')
print(f'Contains "financials_export_nwn": {"financials_export_nwn" in zion_file.name.lower()}')
print(f'Contains generic "financials_export": {"financials_export" in zion_file.name.lower()}')

print()
print('=== EXPECTED RESULTS ===')
print('✅ ZION file should be valid for ZION: True')
print('✅ ZION file should be valid for NWN: False (FIXED!)')
print('✅ This prevents cross-contamination between tickers')

# Clean up test file
zion_file.unlink()
