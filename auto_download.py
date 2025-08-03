import os
import sys
import webbrowser
import time
import shutil
import glob
from pathlib import Path

def get_default_download_folder():
    """Get the default download folder for the current user."""
    user_home = Path.home()
    download_folder = user_home / "Downloads"
    
    if download_folder.exists():
        return str(download_folder)
    return None

def find_recent_xlsx_files(download_folder, minutes_back=2):
    """Find XLSX files modified in the last few minutes."""
    if not download_folder or not os.path.exists(download_folder):
        return []
    
    current_time = time.time()
    cutoff_time = current_time - (minutes_back * 60)
    
    xlsx_pattern = os.path.join(download_folder, "*.xlsx")
    xlsx_files = glob.glob(xlsx_pattern)
    
    recent_files = []
    for file_path in xlsx_files:
        try:
            mod_time = os.path.getmtime(file_path)
            if mod_time > cutoff_time:
                recent_files.append(file_path)
        except OSError:
            continue
    
    return recent_files

def copy_file_to_local(source_path, local_dir="./downloaded_files"):
    """Copy a file from downloads to local directory."""
    try:
        os.makedirs(local_dir, exist_ok=True)
        
        filename = os.path.basename(source_path)
        destination_path = os.path.join(local_dir, filename)
        
        # Handle duplicate filenames
        counter = 1
        base_name, ext = os.path.splitext(filename)
        while os.path.exists(destination_path):
            new_filename = f"{base_name}_{counter}{ext}"
            destination_path = os.path.join(local_dir, new_filename)
            counter += 1
        
        shutil.copy2(source_path, destination_path)
        print(f"✅ Copied: {filename} -> {destination_path}")
        return destination_path
        
    except Exception as e:
        print(f"❌ Error copying file {source_path}: {e}")
        return None

def open_stockrow_and_monitor(ticker_symbol, monitor_duration=60):
    """
    Open StockRow download URL and monitor for downloaded files.
    
    Args:
        ticker_symbol (str): The stock ticker symbol
        monitor_duration (int): How long to monitor for downloads (seconds)
    """
    # Create the URL and open browser
    url = f"https://stockrow.com/vector/exports/financials/{ticker_symbol}?direction=desc"
    
    print(f"Opening download link for {ticker_symbol}...")
    print(f"URL: {url}")
    
    # Open browser
    webbrowser.open(url)
    print("✅ Browser opened! The download should start automatically.")
    print("💡 Downloading the file manually in your browser...")
    
    # Get download folder
    download_folder = get_default_download_folder()
    if not download_folder:
        print("❌ Could not find default download folder!")
        return None
    
    print(f"\n📁 Monitoring downloads folder: {download_folder}")
    print(f"⏱️  Will monitor for {monitor_duration} seconds...")
    print("🔍 Looking for new XLSX files...\n")
    
    local_dir = "./downloaded_files"
    os.makedirs(local_dir, exist_ok=True)
    
    start_time = time.time()
    last_check_time = start_time
    copied_files = []
    
    try:
        while time.time() - start_time < monitor_duration:
            current_time = time.time()
            
            # Check every 3 seconds
            if current_time - last_check_time >= 3:
                recent_files = find_recent_xlsx_files(download_folder, minutes_back=1)
                
                for file_path in recent_files:
                    if file_path not in copied_files:
                        # Check if file might be related to our ticker
                        filename = os.path.basename(file_path).upper()
                        if ticker_symbol.upper() in filename or "financials" in filename.lower():
                            print(f"🎯 Found potential match: {os.path.basename(file_path)}")
                            copied_path = copy_file_to_local(file_path, local_dir)
                            if copied_path:
                                copied_files.append(file_path)
                                print(f"📊 File size: {os.path.getsize(file_path)} bytes")
                                return copied_path
                        else:
                            # Copy any recent XLSX file just in case
                            print(f"📄 Found XLSX file: {os.path.basename(file_path)}")
                            copied_path = copy_file_to_local(file_path, local_dir)
                            if copied_path:
                                copied_files.append(file_path)
                                print(f"📊 File size: {os.path.getsize(file_path)} bytes")
                                return copied_path
                
                last_check_time = current_time
                
                # Show progress every 15 seconds
                elapsed = int(current_time - start_time)
                if elapsed > 0 and elapsed % 15 == 0:
                    remaining = monitor_duration - elapsed
                    print(f"⏳ Still monitoring... {remaining} seconds remaining")
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
    
    if copied_files:
        print(f"\n✅ Monitoring complete. Files saved to: {os.path.abspath(local_dir)}")
        return copied_files[-1]  # Return the last copied file
    else:
        print(f"\n📭 No XLSX files detected during monitoring period.")
        print(f"💡 If you downloaded the file, check your Downloads folder and manually copy it to:")
        print(f"   {os.path.abspath(local_dir)}")
        return None

def get_ticker_from_user():
    """Prompt the user to enter a ticker symbol."""
    while True:
        ticker = input("Enter the ticker symbol (e.g., AAPL, BRK.B, TSLA): ").strip().upper()
        if ticker:
            return ticker
        else:
            print("Please enter a valid ticker symbol.")

def main():
    """Main function to run the script."""
    print("StockRow Auto Download & Monitor")
    print("=" * 35)
    
    # Get ticker symbol from user input or command line argument
    ticker_symbol = None
    for arg in sys.argv[1:]:
        if not arg.startswith('-'):
            ticker_symbol = arg.upper()
            break
    
    if ticker_symbol:
        print(f"Using ticker symbol from command line: {ticker_symbol}")
    else:
        ticker_symbol = get_ticker_from_user()
    
    # Check for monitor duration argument
    monitor_duration = 60  # Default 60 seconds
    if "--duration" in sys.argv:
        try:
            duration_index = sys.argv.index("--duration") + 1
            if duration_index < len(sys.argv):
                monitor_duration = int(sys.argv[duration_index])
        except (ValueError, IndexError):
            pass
    
    print(f"\n🚀 Starting download process for {ticker_symbol}...")
    
    # Open browser and monitor for downloads
    result = open_stockrow_and_monitor(ticker_symbol, monitor_duration)
    
    if result:
        print(f"\n🎉 Success! File saved locally.")
    else:
        print(f"\n💡 If the file downloaded but wasn't detected automatically,")
        print(f"   you can manually copy it to the './downloaded_files' folder.")
    
    print("\n📖 Usage examples:")
    print("  python auto_download.py AAPL")
    print("  python auto_download.py TSLA --duration 120")
    print("  python auto_download.py BRK.B")

if __name__ == "__main__":
    main()
