# Import the necessary libraries
from binance.client import Client
from datetime import datetime, timedelta

# Load the API key and secret from the Secrets.py file
from Secrets import API_KEY, API_SECRET

# Create an instance of the Binance Client using the API key and secret
client = Client(API_KEY, API_SECRET)

# Retrieve information on all futures trading symbols from Binance
futures_exchange_info = client.futures_exchange_info()

# Create a list to store the relevant trading pairs information
relevant_pairs = []

# Calculate the volatility and volume of each trading pair
for info in futures_exchange_info['symbols']:
    symbol = info['symbol']
    if symbol.endswith('USDT'):
        # Get historical price data for the last 24 hours
        start_time = int((datetime.now() - timedelta(days=1)).timestamp()) * 1000
        end_time = int(datetime.now().timestamp()) * 1000
        klines = client.futures_klines(
            symbol=symbol, 
            interval=Client.KLINE_INTERVAL_1HOUR, 
            startTime=start_time,
            endTime=end_time
        )

        # Calculate the total volume by summing the volume of each candle (hourly data)
        volume = sum(float(kline[5]) for kline in klines)

        # Calculate the percentage price change from 24 hours ago to the last price
        last_price = float(klines[-1][4])
        prev_price = float(klines[0][4])
        price_change_percent = ((last_price - prev_price) / prev_price) * 100

        # Append the symbol, volume, and price change percentage to the list
        relevant_pairs.append({
            'symbol': symbol, 
            'volume': volume, 
            'price_change_percent': price_change_percent
        })

# Sort the trading pairs by volume and price change percentage in descending order
relevant_pairs.sort(
    key=lambda x: (x['volume'], x['price_change_percent']), 
    reverse=True
)

# Select the top 6 most relevant trading pairs
top_pairs = relevant_pairs[:6]

# Print the 6 most relevant trading pairs based on volume and price change
print("The 6 most relevant pairs based on volume and volatility:")
for pair in top_pairs:
    print(pair['symbol'], "- Volume:", pair['volume'], "- Price Change Percent:", pair['price_change_percent'])
