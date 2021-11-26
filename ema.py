import matplotlib.pyplot as plt
import pandas as pd
from math import isnan

plt.style.use("dark_background")

def EMA(ma_1, ma_2, file, chart=0):
    
    data = pd.read_csv(file)

    ema1 = [data['Close'].iloc[:ma_1].mean() for _ in range(ma_1)]
    for i in range(ma_1, len(data)):
        ema1.append(ema1[i-1]+(2/(ma_1+1))*(data['Close'].iloc[i]-ema1[i-1]))
    data[f'EMA_{ma_1}'] = ema1

    ema2 = [data['Close'].iloc[:ma_2].mean() for _ in range(ma_2)]
    for i in range(ma_2, len(data)):
        ema2.append(ema2[i-1]+(2/(ma_2+1))*(data['Close'].iloc[i]-ema2[i-1]))
    data[f'EMA_{ma_2}'] = ema2

    data = data[ma_2:]

    bnh = data.Close.iloc[-1]/data.Close.iloc[0]*100

##    plt.plot(data['Close'], label="Share Price", color="lightgray")
##    plt.plot(data[f'EMA_{ma_1}'], label=f"EMA_{ma_1}", color="orange")
##    plt.plot(data[f'EMA_{ma_2}'], label=f"EMA_{ma_2}", color="purple")
##    plt.legend(loc="upper left")
##    plt.show()

    buy_signals = []
    sell_signals = []
    trigger = 0

    last_buy = float('nan')

    for x in range(len(data)):
        if data[f'EMA_{ma_1}'].iloc[x] > data[f'EMA_{ma_2}'].iloc[x] and trigger != 1:
            buy_signals.append(data['Close'].iloc[x])
            sell_signals.append(float('nan'))
            trigger = 1
            last_buy = data['Close'].iloc[x]
        elif data[f'EMA_{ma_1}'].iloc[x] < data[f'EMA_{ma_2}'].iloc[x] and trigger != -1:
            buy_signals.append(float('nan'))
            sell_signals.append(data['Close'].iloc[x])
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
    ticker = file.split('\\')[-1].split('.')[0]

    if chart:
        plt.plot(data['Close'], label="Share Price", linewidth=1, alpha=0.25)
        plt.plot(data[f'EMA_{ma_1}'], label=f"EMA_{ma_1}", color="orange", linestyle="--")
        plt.plot(data[f'EMA_{ma_2}'], label=f"EMA_{ma_2}", color="pink", linestyle="--")
        plt.scatter(data.index, data['Buy Signals'], label="Buy Signal", marker="^", color="#00ff00", zorder=2)
        plt.scatter(data.index, data['Sell Signals'], label="Sell Signal", marker="v", color="#ff0000", zorder=2)
        plt.title(f'{ticker}: ({ma_1}, {ma_2}) - {takeaway}% ROI vs {bnh}% BnH')
        plt.legend(loc="upper left")
        plt.show()
    
    vs_bnh = round((takeaway / bnh)*100, 2)
    print(f'{ticker} | ({ma_1}, {ma_2}): {takeaway} Take, {bnh} BnH, {vs_bnh}% BnH ')

# binance takes 0.075% from each transaction, so the below % is what you would
# multiply takeaway by on each step of return calculation by to simulate fees
# 0.99925 * 

# change prefix to location of your csvs
filepath_prefix = r'C:\Users\kylea\Documents\trade_bot\reenforcement_learning\csvs'

symbol_pool = ['DOGE/USDT', 'BTC/USDT', 'ETH/USDT', 'BNB/USDT',
               'VET/USDT', 'ALGO/USDT', 'SUSHI/USDT', 'MANA/USDT',
               'SOL/USDT', 'ADA/USDT', 'EGLD/USDT', 'LTC/USDT',
               'AMP/USDT', 'ATOM/USDT', 'ENJ/USDT']
crypto_tickers = [s.split('/')[0] for s in symbol_pool]
inc_pool = ['1m', '5m', '15m', '30m', '1h', '1d', '1w']

def path_ify(symbol, inc):
    filepath = filepath_prefix + '\\' + symbol + '_' + inc + '.csv'
    return filepath


def main():
    for inc in inc_pool[1:-1]:
        print(inc + ' cohort...')
        file_names = [path_ify(crypto_ticker, inc) for crypto_ticker in crypto_tickers]
        for file in file_names:
            EMA(12, 26, file)
            EMA(50, 200, file)
main()
#EMA(12, 26, 'SUSHI.csv', chart=1)

