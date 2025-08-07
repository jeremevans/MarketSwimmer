#!/usr/bin/env python3
"""
MarketSwimmer Cleanup Script
Removes analysis output folders and text files from prior runs
"""

import os
import shutil
from pathlib import Path

def cleanup_marketswimmer():
    """Remove analysis output folders and text files from MarketSwimmer runs."""
    
    print("MarketSwimmer Cleanup Script")
    print("Removing analysis output folders and text files...")
    print()
    
    # Define folders to delete
    folders_to_delete = [
        "analysis_output",
        "charts", 
        "data",
        "downloaded_files"
    ]
    
    # Delete folders if they exist
    for folder in folders_to_delete:
        if os.path.exists(folder):
            print(f"Deleting folder: {folder}")
            try:
                shutil.rmtree(folder)
                print(f"✓ Deleted: {folder}")
            except Exception as e:
                print(f"✗ Error deleting {folder}: {e}")
        else:
            print(f"✓ Folder not found (already clean): {folder}")
    
    print()
    
    # Delete all .txt files in the base directory
    txt_files = list(Path(".").glob("*.txt"))
    if txt_files:
        print("Deleting .txt files in base directory:")
        for file in txt_files:
            print(f"  - {file.name}")
            try:
                file.unlink()
            except Exception as e:
                print(f"✗ Error deleting {file.name}: {e}")
        print(f"✓ Deleted {len(txt_files)} .txt files")
    else:
        print("✓ No .txt files found in base directory")
    
    print()
    print("Cleanup completed successfully!")
    print("All analysis output folders and text files have been removed.")

if __name__ == "__main__":
    cleanup_marketswimmer()
