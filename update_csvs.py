import datetime as dt
import pandas as pd

def get_isotime(x):
    return dt.datetime.fromtimestamp(int(str(x)[:10])).isoformat()

def get_klines_iter(tradepair, interval, start, limit=1000):
    df = pd.DataFrame()     
    symbols = tradepair.split('/')
    startDate = start
    proceed = True
    while proceed:
        url = 'https://api.binance.com/api/v3/klines?symbol=' + tradepair.replace('/','') + '&interval=' + interval + '&startTime=' + str(startDate) + '&limit=' + str(limit)
        df2 = pd.read_json(url)
        df2.insert(1,'Opentime_ISO',None)
        df2.insert(1,'Pair',tradepair)
        df2.insert(2,'Base',symbols[0])
        df2.insert(3,'Quote',symbols[1])
        df2.insert(11,'Closetime_ISO',None)
        df2.columns = ['Opentime', 'Pair',  'Base', 'Quote', 'Opentime_ISO',
                       'Open', 'High', 'Low', 'Close', 'Volume', 'Closetime',
                       'Closetime_ISO', 'Quote asset volume', 'Number of trades',
                       'Taker by base', 'Taker buy quote', 'Ignore']
        df2['Opentime_ISO'] = df2.Opentime.apply(get_isotime)
        df2['Closetime_ISO'] = df2['Closetime'].apply(get_isotime)
        df2.drop(columns=['Ignore'], inplace=True)
        if startDate != start and startDate == int(str(df2.Opentime.tail(1).iloc[0])):
            proceed = False
            break
        df = pd.concat([df, df2], axis=0, ignore_index=False, keys=None)
        startDate = int(str(df2.Opentime.tail(1).iloc[0]))
        print(df.Opentime.count())
        print(dt.datetime.fromtimestamp(int(str(startDate)[:10])).isoformat())
    return df

def csv_inator(symbol, inc, days):
    startTime = round((dt.datetime.now() - dt.timedelta(days=days)).timestamp()*1000)

    symbolname = symbol.split('/')[0]

    # change this to the path to folder you want to write csv into
    filepath = r'C:\Users\kylea\Documents\trade_bot\reenforcement_learning\csvs'
    filepath += '\\' + symbolname + '_' + inc
    filepath += '.csv'
    
    print(f'writing {filepath}...')
    results = get_klines_iter(symbol, inc, startTime, limit=1000)
    results.to_csv(filepath, index=False)
    print('done')

symbol_pool = ['DOGE/USDT', 'BTC/USDT', 'ETH/USDT', 'BNB/USDT',
               'VET/USDT', 'ALGO/USDT', 'SUSHI/USDT', 'MANA/USDT',
               'SOL/USDT', 'ADA/USDT', 'EGLD/USDT', 'LTC/USDT',
               'AMP/USDT', 'ATOM/USDT', 'ENJ/USDT']

inc_pool = ['1m', '5m', '15m', '30m', '1h', '1d', '1w']
days_pool = [14, 90, 180, 365, 365*2, 365*2, 365*2]

def onne(sym):
    '''creates a csv in every increment for specified symbol'''
    for i in range(len(inc_pool)):
        csv_inator(sym, inc_pool[i], days_pool[i])

def main():
    '''does onne for all symbols in pool'''
    for symbol in symbol_pool:
        for i in range(len(inc_pool)):
            csv_inator(symbol, inc_pool[i], days_pool[i])
        
##onne('BNB/USDT')
main()



