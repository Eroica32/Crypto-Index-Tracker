from datetime import datetime
import pandas as pd
import coinmarketcapapi

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

# establish connection
cmc = coinmarketcapapi.CoinMarketCapAPI('ece06e3e-37d3-4877-808b-48ef88bb6a6a')

# information about coins in my index
coinsInMyIndex=['ETH', 'BNB', 'XRP', 'ADA', 'SOL', 'DOGE', 'DOT', 
'MATIC', 'SHIB', 'AVAX', 'UNI', 'ETC', 'LTC', 'ATOM','NEAR', 'LINK', 
'CRO', 'XLM', 'FLOW', 'VET']
coinID=[1027,1839,52,2010,5426,74,6636,3890,5994,5805,7083,1321,2,3794,6535,1975,3635,512,4558,3077]

# Add all coin information from CMC Json to DataFrame
jsonDataBTC = cmc.cryptocurrency_quotes_latest(symbol='BTC', convert='CAD')
indexData = pd.DataFrame(jsonDataBTC.data).transpose()
getListing(coinsInMyIndex)

priceTracking = indexData[['name', 'symbol', 'total_supply', 'quote']]
priceTracking['quote'] = priceTracking['quote'].to_dict()
priceTracking['MarketCap'] = priceTracking['total_supply'].astype(float) * priceTracking['quote']['CAD']['price'] #TODO check how to get price

# priceTracking.to_csv('PriceData' + str(datetime.now().date()) + '.csv')