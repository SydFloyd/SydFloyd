import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
import pandas_datareader as web
from math import isnan

yf.pdr_override()

plt.style.use("dark_background")

def avg_dual(ma_1, ma_2, years, ticker):
    '''run sma-crossover strategy on day-wise Yahoo Finance data'''
    start = dt.datetime.now() - dt.timedelta(days=365*years)
    end = dt.datetime.now()

    data = web.get_data_yahoo(ticker, start, end)

    data.head()

    data[f'SMA_{ma_1}'] = data['Adj Close'].rolling(window=ma_1).mean()
    data[f'SMA_{ma_2}'] = data['Adj Close'].rolling(window=ma_2).mean()

    data = data.iloc[ma_2:]

    plt.plot(data['Adj Close'], label="Share Price", color="lightgray")
    plt.plot(data[f'SMA_{ma_1}'], label=f"SMA_{ma_1}", color="orange")
    plt.plot(data[f'SMA_{ma_2}'], label=f"SMA_{ma_2}", color="purple")
    plt.legend(loc="upper left")
    plt.show()

    buy_signals = []
    sell_signals = []
    buys_only = []
    sells_only = []
    trigger = 0

    for x in range(len(data)):
        if data[f'SMA_{ma_1}'].iloc[x] > data[f'SMA_{ma_2}'].iloc[x] and trigger != 1:
            buy_signals.append(data['Adj Close'].iloc[x])
            buys_only.append(data['Adj Close'].iloc[x])
            sell_signals.append(float('nan'))
            trigger = 1
        elif data[f'SMA_{ma_1}'].iloc[x] < data[f'SMA_{ma_2}'].iloc[x] and trigger != -1:
            buy_signals.append(float('nan'))
            sell_signals.append(data['Adj Close'].iloc[x])
            sells_only.append(data['Adj Close'].iloc[x])
            trigger = -1
        else:
            buy_signals.append(float('nan'))
            sell_signals.append(float('nan'))

    data['Buy Signals'] = buy_signals
    data['Sell Signals'] = sell_signals


    last_buy = 0
    bought = 0
    takeaway = 1

    for x in range(len(data)):
        if not isnan(data['Buy Signals'].iloc[x]) and not bought:
            last_buy = data['Buy Signals'].iloc[x]
            bought = 1
        if not isnan(data['Sell Signals'].iloc[x]) and bought:
            takeaway = (data['Sell Signals'].iloc[x] / last_buy) * takeaway
            bought = 0

    takeaway = takeaway * 100

    plt.plot(data['Adj Close'], label="Share Price", linewidth=1, alpha=0.25)
    plt.plot(data[f'SMA_{ma_1}'], label=f"SMA_{ma_1}", color="orange", linestyle="--")
    plt.plot(data[f'SMA_{ma_2}'], label=f"SMA_{ma_2}", color="pink", linestyle="--")
    plt.scatter(data.index, data['Buy Signals'], label="Buy Signal", marker="^", color="#00ff00", zorder=2)
    plt.scatter(data.index, data['Sell Signals'], label="Sell Signal", marker="v", color="#ff0000", zorder=2)
    plt.title(f'({ma_1}, {ma_2}) - {takeaway}% ROI')
    plt.legend(loc="upper left")
    plt.show()

#avg_dual(ma_1, ma_2, years, ticker)
avg_dual(7, 21, 2, 'CRO-USD')




stock_tickers = ['MSFT', 'FB', 'IBM', 'AAPL', 'MMM', 'XOM', 'COKE', 'AMZN']
crypto_tickers = ['DOGE', 'BTC', 'ETH', 'BNB', 'VET']

all_tickers = stock_tickers + crypto_tickers





                 
