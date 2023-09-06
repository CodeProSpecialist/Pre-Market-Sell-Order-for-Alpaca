import alpaca_trade_api as tradeapi
import yfinance as yf

# Initialize Alpaca API with your credentials
api = tradeapi.REST('YOUR_API_KEY', 'YOUR_SECRET_KEY', base_url='https://paper-api.alpaca.markets')  # Use paper trading for testing

def main_menu():
    print("1. Print All Owned Stocks")
    print("2. Sell Stock during Pre-Market")
    print("3. Exit")

def print_owned_stocks():
    positions = api.list_positions()
    if positions:
        print("Owned Stocks:")
        for i, position in enumerate(positions):
            print(f"{i + 1}. {position.symbol} - Shares: {position.qty}, Avg. Price: ${position.avg_entry_price}")
    else:
        print("You don't own any stocks.")

def sell_stock(symbol):
    position = api.get_position(symbol)
    if position:
        current_quantity = int(position.qty)

        # Fetch the current price using yfinance
        stock_info = yf.Ticker(symbol)
        current_stock_price = stock_info.history(period="1d")["Close"].iloc[0]

        print(f"Symbol: {symbol}")
        print(f"Shares Owned: {current_quantity}")
        print(f"Avg. Price Paid: ${position.avg_entry_price}")
        print(f"Current Price: ${current_stock_price}")  # Display the current price
        shares_to_sell = int(input("Enter the number of shares to sell: "))

        if shares_to_sell <= current_quantity:
            order_total = shares_to_sell * current_stock_price
            print(f"Order Total: ${order_total}")
            proceed = input("Proceed to sell during pre-market? (Yes/No): ").lower()
            if proceed == "yes":
                submit_pre_market_sell_order(symbol, shares_to_sell)
            else:
                print("Sell order canceled.")
        else:
            print("You can't sell more shares than you own.")
    else:
        print(f"You don't own any shares of {symbol}.")

def submit_pre_market_sell_order(symbol, quantity):
    # The function to submit a pre-market sell order (as previously discussed)
    pass

while True:
    main_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        print_owned_stocks()
    elif choice == "2":
        symbol = input("Enter the stock symbol you want to sell: ")
        sell_stock(symbol)
    elif choice == "3":
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please choose a valid option.")
