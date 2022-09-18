import coinmarketcapapi

class APIData:
    def __init__(self, accessCode, targetCoins):
        '''
        accessCode: code requires to establish connection with CMC (string)
        targetCoins: CSV file location of desired coins in the index
        '''
        self.accessCode = accessCode
        self.targetCoins = targetCoins
    def establishConnection():
        try:
            cmc = coinmarketcapapi.CoinMarketCapAPI('ece06e3e-37d3-4877-808b-48ef88bb6a6a')
        except:
            return 'connection error, check access code'
