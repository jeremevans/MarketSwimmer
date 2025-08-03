import os
import shutil
import time
import sys
from pathlib import Path
import glob

def get_default_download_folder():
    """
    Get the default download folder for the current user.
    
    Re    print("[HELP] Usage examples:")
    print("  python monitor_downloads.py          # Continuous monitoring")
    print("  python monitor_downloads.py --check  # One-time check")

if __name__ == "__main__":
    main()
        str: Path to the default download folder
    """
    # For Windows, the default download folder is usually in the user's profile
    user_home = Path.home()
    download_folder = user_home / "Downloads"
    
    if download_folder.exists():
        return str(download_folder)
    else:
        # Fallback to common alternatives
        alternatives = [
            user_home / "Download",
            Path("C:/Users") / os.getenv("USERNAME", "") / "Downloads"
        ]
        
        for alt in alternatives:
            if alt.exists():
                return str(alt)
    
    return None

def find_recent_xlsx_files(download_folder, minutes_back=5):
    """
    Find XLSX files modified in the last few minutes.
    
    Args:
        download_folder (str): Path to the download folder
        minutes_back (int): How many minutes back to look for files
    
    Returns:
        list: List of file paths that were recently modified
    """
    if not download_folder or not os.path.exists(download_folder):
        return []
    
    current_time = time.time()
    cutoff_time = current_time - (minutes_back * 60)  # Convert minutes to seconds
    
    # Look for XLSX files
    xlsx_pattern = os.path.join(download_folder, "*.xlsx")
    xlsx_files = glob.glob(xlsx_pattern)
    
    recent_files = []
    for file_path in xlsx_files:
        try:
            # Get file modification time
            mod_time = os.path.getmtime(file_path)
            if mod_time > cutoff_time:
                recent_files.append(file_path)
        except OSError:
            # Skip files that can't be accessed
            continue
    
    return recent_files

def copy_file_to_local(source_path, local_dir="./downloaded_files"):
    """
    Copy a file from the download folder to a local directory.
    
    Args:
        source_path (str): Path to the source file
        local_dir (str): Local directory to copy the file to
    
    Returns:
        str: Path to the copied file if successful, None if failed
    """
    try:
        # Create local directory if it doesn't exist
        os.makedirs(local_dir, exist_ok=True)
        
        # Get the filename
        filename = os.path.basename(source_path)
        destination_path = os.path.join(local_dir, filename)
        
        # If file already exists, create a unique name
        counter = 1
        base_name, ext = os.path.splitext(filename)
        while os.path.exists(destination_path):
            new_filename = f"{base_name}_{counter}{ext}"
            destination_path = os.path.join(local_dir, new_filename)
            counter += 1
        
        # Copy the file
        shutil.copy2(source_path, destination_path)
        
        print(f"[OK] Copied: {filename} -> {destination_path}")
        return destination_path
        
    except Exception as e:
        print(f"[ERROR] Error copying file {source_path}: {e}")
        return None

def monitor_downloads(check_interval=10, max_checks=60):
    """
    Monitor the download folder for new XLSX files and copy them locally.
    
    Args:
        check_interval (int): Seconds between checks
        max_checks (int): Maximum number of checks before stopping
    """
    download_folder = get_default_download_folder()
    
    if not download_folder:
        print("[ERROR] Could not find default download folder!")
        return
    
    print(f"[FOLDER] Monitoring download folder: {download_folder}")
    print(f"[CHECK] Checking every {check_interval} seconds for new XLSX files...")
    print(f"[TIME] Will monitor for {max_checks * check_interval} seconds total")
    print("Press Ctrl+C to stop monitoring\n")
    
    local_dir = "./downloaded_files"
    os.makedirs(local_dir, exist_ok=True)
    
    copied_files = set()  # Keep track of files we've already copied
    
    try:
        for check_num in range(max_checks):
            recent_files = find_recent_xlsx_files(download_folder, minutes_back=2)
            
            new_files = []
            for file_path in recent_files:
                file_id = f"{file_path}_{os.path.getmtime(file_path)}"
                if file_id not in copied_files:
                    new_files.append(file_path)
                    copied_files.add(file_id)
            
            if new_files:
                print(f"[NEW] Found {len(new_files)} new XLSX file(s):")
                for file_path in new_files:
                    copied_path = copy_file_to_local(file_path, local_dir)
                    if copied_path:
                        print(f"   [SIZE] Size: {os.path.getsize(file_path)} bytes")
                print()
            else:
                if check_num % 6 == 0:  # Print status every minute
                    print(f"[WAIT] Still monitoring... ({check_num + 1}/{max_checks})")
            
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        print("\n[STOP] Monitoring stopped by user")
    
    print(f"\n[DONE] Monitoring complete. Local files saved to: {os.path.abspath(local_dir)}")

def check_recent_downloads():
    """
    Check for recent downloads without continuous monitoring.
    """
    download_folder = get_default_download_folder()
    
    if not download_folder:
        print("[ERROR] Could not find default download folder!")
        return
    
    print(f"[FOLDER] Checking download folder: {download_folder}")
    recent_files = find_recent_xlsx_files(download_folder, minutes_back=10)
    
    if recent_files:
        print(f"[NEW] Found {len(recent_files)} recent XLSX file(s):")
        local_dir = "./downloaded_files"
        
        for file_path in recent_files:
            file_size = os.path.getsize(file_path)
            mod_time = time.ctime(os.path.getmtime(file_path))
            print(f"   [FILE] {os.path.basename(file_path)} ({file_size} bytes, modified: {mod_time})")
            
            copied_path = copy_file_to_local(file_path, local_dir)
        
        print(f"\n[DONE] Files copied to: {os.path.abspath(local_dir)}")
    else:
        print("[EMPTY] No recent XLSX files found in downloads folder")

def main():
    """
    Main function to run the script.
    """
    print("StockRow Download Monitor")
    print("=" * 30)
    
    if len(sys.argv) > 1 and sys.argv[1] in ['--check', '-c']:
        # One-time check mode
        check_recent_downloads()
    else:
        # Continuous monitoring mode
        print("Choose monitoring mode:")
        print("1. Monitor continuously (default)")
        print("2. Check once for recent files")
        
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "2":
            check_recent_downloads()
        else:
            monitor_downloads()
    
    print("\n[HELP] Usage examples:")
    print("  python monitor_downloads.py          # Continuous monitoring")
    print("  python monitor_downloads.py --check  # One-time check")

if __name__ == "__main__":
    main()
