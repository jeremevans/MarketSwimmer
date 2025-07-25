import yfinance as yf

def get_option_price(ticker, expiry_date, strike_price, option_type):
    stock = yf.Ticker(ticker)
    options = stock.option_chain(expiry_date)
    
    if option_type == 'call':
        option_data = options.calls
    elif option_type == 'put':
        option_data = options.puts
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
    
    specific_option = option_data[option_data['strike'] == strike_price]
    if not specific_option.empty:
        bid = specific_option['bid'].iloc[0]
        ask = specific_option['ask'].iloc[0]
        last = specific_option['lastPrice'].iloc[0]
        average_price = (bid + ask + last) / 3
        return bid, ask, last, average_price
    else:
        return None, None, None, None

def main():
    ticker = 'CVNA'
    expiry_date = '2025-07-25'
    strike_price = 350.00
    option_type = 'put'
    
    bid, ask, last, average_price = get_option_price(ticker, expiry_date, strike_price, option_type)
    if bid is not None:
        print(f"Bid: {bid}, Ask: {ask}, Last: {last}, Average: {average_price}")
    else:
        print("Option not found")

if __name__ == "__main__":
    main()