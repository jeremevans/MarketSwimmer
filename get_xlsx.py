import os
import sys
import webbrowser

def open_stockrow_download(ticker_symbol, output_dir="./downloads"):
    """
    Open StockRow download URL in browser for manual download.
    
    Args:
        ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL', 'BRK.B')
        output_dir (str): Directory where user should save the downloaded file
    
    Returns:
        str: The output directory path
    """
    # Create the URL with the ticker symbol
    url = f"https://stockrow.com/vector/exports/financials/{ticker_symbol}?direction=desc"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Opening download link for {ticker_symbol}...")
    print(f"URL: {url}")
    print(f"📁 Please save the file to: {os.path.abspath(output_dir)}")
    
    # Open the URL in the default browser
    webbrowser.open(url)
    
    print("✅ Browser opened! The download should start automatically.")
    print("💡 If the download doesn't start, right-click and 'Save As' to your downloads folder.")
    
    return output_dir

def get_ticker_from_user():
    """
    Prompt the user to enter a ticker symbol.
    
    Returns:
        str: The ticker symbol entered by the user
    """
    while True:
        ticker = input("Enter the ticker symbol (e.g., AAPL, BRK.B, TSLA): ").strip().upper()
        if ticker:
            return ticker
        else:
            print("Please enter a valid ticker symbol.")

def main():
    """
    Main function to run the script.
    """
    print("StockRow Manual Download Helper")
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
    
    # Get output directory (optional)
    output_dir = "./downloads"
    
    # Open browser for manual download
    download_dir = open_stockrow_download(ticker_symbol, output_dir)
    
    print(f"\n🌐 Browser opened for manual download of {ticker_symbol}")
    print(f"📁 Download location: {os.path.abspath(download_dir)}")
    print("\n📖 Usage examples:")
    print("  python get_xlsx.py AAPL")
    print("  python get_xlsx.py TSLA")
    print("  python get_xlsx.py BRK.B")

if __name__ == "__main__":
    main()