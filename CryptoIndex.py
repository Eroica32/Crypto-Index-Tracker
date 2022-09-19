from distutils import core
import json
import pandas as pd
import coinmarketcapapi
import matplotlib.pyplot as plt
import seaborn as sns

# information about coins in my index (no stable coins)
targetCoin = pd.read_csv('TargetCoin.csv')
symbols = list(targetCoin['CoinName'])

# establish connection
try:
  cmc = coinmarketcapapi.CoinMarketCapAPI('ece06e3e-37d3-4877-808b-48ef88bb6a6a')
except:
  print('connection error, check access code')
# TODO make it so that it stores all my data
# TODO maybe put get symbol somewhere else
def getSymbol():
  '''get a dataframe of coin names and symbols'''
  data_id_map = cmc.cryptocurrency_map()
  symbolData = pd.DataFrame(data_id_map.data)
  symbolData.set_index('name')
  print(symbolData)
def getListing(coin, datatype='symbol'):
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
def cleanQuoteColumn(df):
  '''extract the price and the market cap'''
  marketCap = dict()
  price = dict()
  counter = 0
  for row in df[['quote']].itertuples():
    tempDict = json.loads(str(str(row[1])[8:len(row[1])-1]).replace("'",'"').replace('None', '0'))
    price[counter] = tempDict['price']
    marketCap[counter] = tempDict['market_cap']
    counter += 1
  coreData['price'] = list(price.values())
  coreData['MarketCap'] = list(marketCap.values())

# Add all coin information from CMC Json to DataFrame
rawData = getListing(symbols)

# Cleaning API Data from CMC TODO fix this, too much writing and reading
coreData = rawData[['name', 'symbol', 'total_supply', 'quote']]
coreData.to_csv('UpdatedCoinInformation.csv')
indexInformation = pd.read_csv('UpdatedCoinInformation.csv')
cleanQuoteColumn(indexInformation)
coreData[['name', 'symbol', 'total_supply', 'MarketCap', 'price']].to_csv('UpdatedCoinInformation.csv')

# Index caluation
totalIndexValue = float(input('How much would you like to put into your index (in CAD): '))
totalValue = coreData['MarketCap'].sum()
tempDict = dict()
counter = 0
for coin in coreData['MarketCap']:
  tempDict[counter] = float(coin) / totalValue
  counter += 1
coreData['Prop in Index'] = list(tempDict.values())
coreData['how much to buy'] = coreData['Prop in Index'] * totalIndexValue
print(coreData['how much to buy'])
print('saved to CryptoIndexSummary.csv')
coreData['how much till index'] =  coreData['how much to buy'] - coreData['price'] * list(targetCoin['myCoins']) 
coreData[['name', 'how much to buy', 'how much till index']].to_csv('CryptoIndexSummary.csv')

# visualization
colors = sns.color_palette('bright')
plt.pie(coreData['how much to buy'], labels=symbols,colors = colors, autopct = '%0.0f%%', labeldistance=1.3)
plt.show()


