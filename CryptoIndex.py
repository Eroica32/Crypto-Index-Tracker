import json
import pandas as pd
import coinmarketcapapi
import wx
import matplotlib.pyplot as plt
import seaborn as sns

# functions
def getSymbol(coinName):
  '''get the symbol of a coin from a coin name'''
  data_id_map = cmc.cryptocurrency_map()
  symbolData = pd.DataFrame(data_id_map.data, columns =['name','symbol'])
  symbolData.set_index('name')
  symbolData_dict = dict(zip(symbolData['name'], symbolData['symbol']))

  for name in symbolData_dict.keys():
    if str.lower(name) == str.lower(coinName):
      return symbolData_dict[name]
  return 'no result'
def getListing(coinSymbol):
  '''request coin information(s) from CMC and
  concatenate them to existing coin info df'''
  global indexData
  for symbol in coinSymbol:
    tempDF = pd.DataFrame(cmc.cryptocurrency_quotes_latest(symbol=symbol, convert='CAD').data).transpose()
    indexData = pd.concat([indexData, tempDF])
def getListingUsingID(coinID):
  '''request coin information(s) from CMC and
  concatenate them to existing coin info df using CMC coin ID'''
  global indexData
  for id in coinID:
    tempDF = pd.DataFrame(cmc.cryptocurrency_quotes_latest(id=id, convert='CAD').data).transpose()
    indexData = pd.concat([indexData, tempDF])
def cleanQuoteColumn(df):
  marketCap = dict()
  price = dict()
  counter = 0
  for row in df[['quote']].itertuples():
    tempDict = json.loads(str(str(row[1])[8:len(row[1])-1]).replace("'",'"').replace('None', '0'))
    price[coinsInMyIndex[counter]] = tempDict['price']
    marketCap[coinsInMyIndex[counter]] = tempDict['market_cap']
    counter += 1
  priceTracking['price'] = list(price.values())
  priceTracking['MarketCap'] = list(marketCap.values())
  
# establish connection
cmc = coinmarketcapapi.CoinMarketCapAPI('ece06e3e-37d3-4877-808b-48ef88bb6a6a')

# information about coins in my index (no stable coins)
# used for Indexing
coinsInMyIndex=['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'SOL', 'DOGE', 'DOT', 
'MATIC', 'SHIB', 'AVAX', 'UNI', 'ETC', 'LTC', 'ATOM','NEAR', 'LINK', 
'CRO', 'XLM', 'FLOW', 'VET'] 
coinID=[1027,1839,52,2010,5426,74,6636,3890,5994,5805,7083,1321,2,3794,6535,1975,3635,512,4558,3077]

# Add all coin information from CMC Json to DataFrame
jsonDataBTC = cmc.cryptocurrency_quotes_latest(symbol='BTC', convert='CAD')
indexData = pd.DataFrame(jsonDataBTC.data).transpose()
getListingUsingID(coinID)

# Cleaning API Data from CMC
priceTracking = indexData[['name', 'symbol', 'total_supply', 'quote']]
cleanQuoteColumn(priceTracking)

# Index caluation
totalIndexValue = float(input('How much would you like to put into your index: '))
totalValue = priceTracking['MarketCap'].sum()
tempDict = dict()
counter = 0
for coin in priceTracking['MarketCap']:
  tempDict[coinsInMyIndex[counter]] = float(coin) / totalValue
  counter += 1
priceTracking['Prop in Index'] = list(tempDict.values())
priceTracking['how much to buy'] = priceTracking['Prop in Index'] * 2000
print(priceTracking['how much to buy'])
print('saved to CryptoIndex.csv')

priceTracking.to_csv('CryptoIndexSummary.csv')
