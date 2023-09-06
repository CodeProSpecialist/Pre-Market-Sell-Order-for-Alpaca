import alpaca_trade_api as tradeapi
import yfinance as yf
import os, sys

# Load environment variables for Alpaca API
APIKEYID = os.getenv('APCA_API_KEY_ID')
APISECRETKEY = os.getenv('APCA_API_SECRET_KEY')
APIBASEURL = os.getenv('APCA_API_BASE_URL')

# Initialize the Alpaca API
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)

global symbol, shares_to_sell, limit_price_number


def main_menu():
    print("")
    print("Pre-market: 4:00am - 9:30am ET Monday thru Friday ")
    print("")
    print("1. Print All Owned Stocks")
    print("2. Sell Stock during Pre-Market")
    print("3. Exit")
    print("")


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
        print(f"Previous Market Closing Price: ${current_stock_price}")  # Display the current price
        print("Remember that the Pre-market price is different than the Previous Market Closing Price. ")
        print("Set a limit price equal to or higher than the current pre-market price.")
        print("To sell more quickly, "
              "set the limit price as exactly the same price as the "
              "current pre-market price.") 
        limit_price_number = float(input("Enter the limit price per share: "))
        shares_to_sell = int(input("Enter the number of shares to sell: "))

        if shares_to_sell <= current_quantity:
            order_total = shares_to_sell * limit_price_number
            print(f"Order Total: ${order_total}")
            proceed = input("Proceed to sell during pre-market? (yes/no): ").lower()
            if proceed == "yes":
                submit_pre_market_sell_order(symbol, shares_to_sell, limit_price_number)  # Pass all three arguments
            else:
                print("Sell order canceled.")
        else:
            print("You can't sell more shares than you own.")
    else:
        print(f"You don't own any shares of {symbol}.")


def submit_pre_market_sell_order(symbol, shares_to_sell , limit_price_number):
    # Get current position
    position = api.get_position(symbol)

    if position:
        current_quantity = int(position.qty)  # Convert to an integer
        current_price = float(api.get_latest_trade(symbol).price)  # Get the last trade price as the current price

        # Define order parameters
        order = {
            'symbol': symbol,
            'qty': shares_to_sell,  # Add current quantity to the sell order
            'side': 'sell',  # Set to 'sell' for a sell order
            'type': 'limit',
            'time_in_force': 'day',
            'limit_price': limit_price_number,  # Set the limit price as the current price
            'extended_hours': True  # Set to true for extended hours trading
        }

        try:
            # Submit the order
            api.submit_order(**order)
            print(f"Sell order for {current_quantity} shares of {symbol} submitted successfully during pre-market hours at {limit_price_number}.")
        except Exception as e:
            print(f"Error submitting sell order: {e}")
    else:
        print(f"No position found for {symbol}.")


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
