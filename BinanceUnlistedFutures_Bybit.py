"""
Script to identify USDT-M tickers that are NOT on Binance Futs but available on Bybit Futs

NOT OPTIMIZED!!!

""" 
__author__ = "ChopTradoor"
__contract__ = "https://twitter.com/ChopTradoor"
__version__ = "1.0.0"

import re
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from pybit.unified_trading import HTTP

bybit_tickers = []
binance_tickers = [info['symbol'] for info in Client().futures_exchange_info()['symbols']]
for item in HTTP().get_tickers(category = "linear").get('result').get('list'):
    bybit_tickers.append(item.get('symbol'))

ticker_difference = []
for ticker in bybit_tickers:
    if ticker not in binance_tickers:
        ticker_difference.append(ticker)

loop = True
while loop: # TODO:Debug why this must be run multiple times to clean up matches for regex search
    current = len(ticker_difference)
    for i in ticker_difference:
        if bool(re.search("perp", i, re.IGNORECASE)) or bool(re.search("-", i, re.IGNORECASE)) or bool(re.search("SHIB", i, re.IGNORECASE)) or bool(re.search("BUSD", i, re.IGNORECASE)):
            ticker_difference.remove(i)
    end = len(ticker_difference)
    if current == end:
        loop = False

with open('ticker_differences_OUTPUT.txt', 'w') as f:
    for line in ticker_difference:
        updated_tradingview_synax = "BYBIT:"+line+".p"
        print(updated_tradingview_synax) 
        f.write(updated_tradingview_synax)
        f.write('\n')