from os import error
from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
import datetime
from matplotlib import pyplot as plt
import numpy as np

import indicators


tickers = si.tickers_sp500()
tickers = [item.replace(".","-") for item in tickers]

index_name = '^GSPC' # S&P 500
start_date = datetime.datetime.now() - datetime.timedelta(days=365)
end_date = datetime.date.today()

# Index Returns
index_df = pdr.get_data_yahoo(index_name, start_date, end_date)
index_df['Percent Change'] = index_df['Adj Close'].pct_change()
index_return = (index_df['Percent Change'] + 1).cumprod()[-1]

for ticker in tickers:
    try:
        df = pdr.get_data_yahoo(ticker, start_date, end_date)
        #df.to_csv(f'historical_data/{ticker}.csv')

        macd, macd_signal = indicators.macd(df)
        rsi = indicators.rsi(df)
        ss = indicators.slow_stochastic(df)

        #Condition 1: Macd buy signal
        condition_1 = macd.iat[-1] >= macd_signal.iat[-1]

        #Condition 2: Slow Stocastics cross 20 line
        condition_2 = ss.iat[-1] < 40

        #Condition 3: RSI > 50
        condition_3 = rsi.iat[-1] >= 50

        conditions = [condition_1, condition_2, condition_3]

        if condition_1 and condition_2 and condition_3:
            print()
            print('--------All BUY: ' + ticker)
            print()
        elif np.count_nonzero(conditions) > 1:
            print('Buy: ' + ticker)
            if condition_1:
                print('  Macd')
            if condition_2:
                print('  Slow Stochastics')
            if condition_3:
                print('  RSI')
            print()
    except KeyError or ValueError:
        print('Could not read ' + ticker + ' data')
        
        


