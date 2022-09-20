import pandas as pd

class IndexCalculation:
    def __init__(self, coreData, totalIndexValue, targetCoins):
        self.coreData = coreData
        self.totalValue = coreData['MarketCap'].sum()
        self.totalIndexValue = totalIndexValue
        self.targetCoins = targetCoins
    def calculateProp(self):
        tempDict = dict()
        counter = 0
        for coin in self.coreData['MarketCap']:
            tempDict[counter] = (float(coin) / self.totalValue) * 100
            counter += 1
        self.coreData['Prop'] = list(tempDict.values())
    def totalCoinValue(self):
        self.coreData['total coin value'] = self.coreData['Prop'] * self.totalIndexValue / 100
    def additionalCapitalNeeded(self):
        self.coreData['additional capital needed'] =  self.coreData['total coin value'] - self.coreData['price'] * list(self.targetCoins['myCoins'])
    def percentTotalCapiptal(self):
        self.coreData['percent capital invested'] = (self.coreData['price'] * list(self.targetCoins['myCoins']) / self.coreData['total coin value']) * 100
    