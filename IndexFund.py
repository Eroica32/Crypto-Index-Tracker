from APIData import APIData
from IndexCalculation import IndexCalculation
from Visualization import Visualization

# initialize API object
# Add all coin information from CMC Json to DataFrame
API = APIData('ece06e3e-37d3-4877-808b-48ef88bb6a6a', 'TargetCoin.csv')
coinSymbols = list(API.targetCoins['CoinName'])
rawData = API.getTargetCoins(API.cmc, coinSymbols)

# extract price and market cap from 'quote'
coreData = API.extractPriceAndMarketCap(rawData[['name', 'symbol', 'total_supply', 'quote']])
coreData[['name', 'symbol', 'total_supply', 'MarketCap', 'price']].to_csv('CoinInformation.csv')

# Index caluation
totalIndexValue = float(input('How much would you like to put into your index (in CAD): '))
index = IndexCalculation(coreData, totalIndexValue, API.targetCoins)
index.calculateProp()
index.totalCoinValue()
index.additionalCapitalNeeded()
index.percentTotalCapiptal()
index.coreData.to_csv('IndexSummary.csv')

# visualization
vis = Visualization()
vis.pieChart(coreData)


