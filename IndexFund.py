from APIData import APIData
from Visualization import Visualization

def indexCalculation(totalIndexValue):
  '''
  calculates the information that are required to build an crypto index
  '''
  totalValue = coreData['MarketCap'].sum()

  tempDict = dict()
  counter = 0
  for coin in coreData['MarketCap']:
    tempDict[counter] = float(coin) / totalValue
    counter += 1
  
  coreData['Prop'] = list(tempDict.values())
  coreData['total coin value'] = coreData['Prop'] * totalIndexValue
  coreData['how much till index'] =  coreData['total coin value'] - coreData['price'] * list(API.targetCoins['myCoins']) 
  coreData['percentage till index'] = 1 - coreData['price'] * list(API.targetCoins['myCoins']) / coreData['total coin value']
  coreData.sort_values(by='percentage till index', ascending=True)
  coreData[['name', 'total coin value', 'how much till index', 'percentage till index']].to_csv('IndexSummary.csv')

# initialize API object
# Add all coin information from CMC Json to DataFrame
API = APIData('ece06e3e-37d3-4877-808b-48ef88bb6a6a', 'TargetCoin.csv')
rawData = API.getTargetCoins(API.cmc, list(API.targetCoins['CoinName']))

# extract price and market cap from 'quote'
coreData = API.extractPriceAndMarketCap(rawData[['name', 'symbol', 'total_supply', 'quote']])
coreData[['name', 'symbol', 'total_supply', 'MarketCap', 'price']].to_csv('CoinInformation.csv')

# Index caluation
totalIndexValue = float(input('How much would you like to put into your index (in CAD): '))
indexCalculation(totalIndexValue)

# visualization
vis = Visualization()
vis.pieChart(coreData)


