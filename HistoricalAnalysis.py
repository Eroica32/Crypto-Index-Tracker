import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

class HistoricalAnalysis:
    def __init__(self, conversionRate):
        self.conversionRate = conversionRate
    def getHistory(self, targetCoin):
        lst = list(targetCoin['CoinName'])
        BTC = yf.Ticker('BTC-USD')
        df = pd.DataFrame(BTC.history(period='max', interval = '1d'))['Date', 'Close']
        df.columns = ['Date', 'BTC-USD']

        for i in range(len(lst)-1):
            if lst[i+1] == 'UNI':
                temp = yf.Ticker("UNI1-USD")
                history = pd.DataFrame(temp.history(period='max', interval='1d'))['Close']
            else:
                temp = yf.Ticker(str(lst[i+1]) + "-USD")
                history = pd.DataFrame(temp.history(period='max', interval='1d'))['Close']
            df[lst[i+1] + '-CAD'] = history * self.conversionRate
        
        return df


