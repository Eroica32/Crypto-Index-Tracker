import coinmarketcapapi
import json
import pandas as pd

class APIData:
    def __init__(self, accessCode, targetCoins):
        '''
        accessCode: code requires to establish connection with CMC (string)
        targetCoins: CSV file location of desired coins in the index
        '''
        self.targetCoins = pd.read_csv(targetCoins)
        self.accessCode = accessCode
        try:
            self.cmc = coinmarketcapapi.CoinMarketCapAPI(self.accessCode)
        except:
            print('connection error, check access code')
    def getSymbol(self, cmc):
        '''get print out of coin names and symbols'''
        data_id_map = cmc.cryptocurrency_map()
        symbolData = pd.DataFrame(data_id_map.data)
        symbolData.set_index('name')
        return symbolData
    def getTargetCoins(self, cmc, coin, datatype='symbol'):
        '''request coin information(s) from CMC and
        concatenate them to existing coin info df using CMC coin ID or coin name'''
        rawData = pd.DataFrame(cmc.cryptocurrency_quotes_latest(symbol=coin[0], convert='CAD').data).transpose()
        if datatype == 'ID':
            for i in range(len(coin)-1):
                i+=1
                tempDF = pd.DataFrame(cmc.cryptocurrency_quotes_latest(id=coin[i], convert='CAD').data).transpose()
                rawData = pd.concat([rawData, tempDF])
        else:
            for i in range(len(coin)-1):
                i+=1
                tempDF = pd.DataFrame(cmc.cryptocurrency_quotes_latest(symbol=coin[i], convert='CAD').data).transpose()
                rawData = pd.concat([rawData, tempDF])
        return rawData
    def extractPriceAndMarketCap(self, coreData):
        '''extract the price and the market cap'''
        marketCap = dict()
        price = dict()
        counter = 0
        for row in coreData[['quote']].itertuples():
            # string to dict
            tempDict = json.loads(str(str(row[1])[8:len(str(row[1]))-1]).replace("'",'"').replace('None', '0'))
            price[counter] = tempDict['price']
            marketCap[counter] = tempDict['market_cap']
            counter += 1
        coreData['price'] = list(price.values())
        coreData['MarketCap'] = list(marketCap.values())
        return coreData
