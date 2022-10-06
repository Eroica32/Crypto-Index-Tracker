import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

class HistoricalAnalysis:
    def __init__(self, conversionRate, YFinanceData):
        self.conversionRate = conversionRate
        self.YFinanceData = None
    def getHistory(self, targetCoin):
        def sliceList(lst, x):
            column = ['Date', 'BTC-CAD']
            for i in range(x):
                column.append(lst[i+1] + "-CAD")
            return column
        lst = list(targetCoin['CoinName'])

        BTC = yf.Ticker('BTC-USD')
        df = pd.DataFrame(BTC.history(period='max', interval = '1d'))
        df.reset_index(inplace=True)
        df = df[['Date', 'Close']]
        df.columns = ['Date', 'BTC-CAD']
        df['BTC-CAD'] = df['BTC-CAD'] * self.conversionRate

        for i in range(len(lst)-1):
            if lst[i+1] == 'UNI':
                temp = yf.Ticker("UNI1-USD")
                history = pd.DataFrame(temp.history(period='max', interval='1d'))
                history.reset_index(inplace=True)
                df = df.merge(pd.DataFrame(history[['Date', 'Close']]), how='left')
                df.columns = sliceList(lst, i+1)
                df[str(lst[i+1]) + "-CAD"] = df[str(lst[i+1]) + "-CAD"] * self.conversionRate
        
            else:
                temp = yf.Ticker(str(lst[i+1]) + "-USD")
                history = pd.DataFrame(temp.history(period='max', interval='1d'))
                history.reset_index(inplace=True)
                df = df.merge(pd.DataFrame(history[['Date', 'Close']]), how='left')
                df.columns = sliceList(lst, i+1)
                df[str(lst[i+1]) + "-CAD"] = df[str(lst[i+1]) + "-CAD"] * self.conversionRate
                
        self.YFinanceData = df.fillna(0)
        return df.fillna(0)


