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
    tempDF = pd.DataFrame(cmc.cryptocurrency_quotes_latest(symbol=symbol, convert='CAD').data)
    pd.concat([indexData, tempDF])

# index calculation

cmc = coinmarketcapapi.CoinMarketCapAPI('ece06e3e-37d3-4877-808b-48ef88bb6a6a')

coinsInMyIndex=['ETH', 'BNB', 'XRP', 'ADA', 'SOL', 'DOGE', 'DOT', 
'MATIC', 'SHIB', 'AVAX', 'UNI', 'ETC', 'LTC', 'ATOM','NEAR', 'LINK', 
'CRO', 'XLM', 'FLOW', 'VET']
jsonDataBTC = cmc.cryptocurrency_quotes_latest(symbol='BTC', convert='CAD')
indexData = pd.DataFrame(jsonDataBTC.data).melt
getListing(coinsInMyIndex)
print(indexData)