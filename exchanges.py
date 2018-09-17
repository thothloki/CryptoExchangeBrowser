import requests, json

exchangeList = ['MapleExchange', 'TradeOgre']
tradingPairs = []

class MapleExchange:
    def getPairs():
        try:
            tradingPairs = []
            URL = 'https://maplechange.com:443//api/v2/markets.json'
            req = requests.get(url = URL)
            markets = req.json()
            for pair in markets:
                tradingPairs.append(pair['name'])
            return tradingPairs
        except:
            pass
        
    def getCoin(selected):
        try:
            pair = str(selected).split('/')
            coin = (str(pair[1]) + str(pair[0])).lower()
            site = 'https://maplechange.com//api/v2/tickers/' + coin + '.json'
            r = requests.get(url = site)
            data = r.json()
            main = pair[0].upper()
            bid = (data['ticker']['buy'])
            ask = (data['ticker']['sell'])
            last = (data['ticker']['last'])
            values = main, bid, ask, last
            return values
        except:
            pass
        
class TradeOgre:
    def getPairs():
        try:
            tradingPairs = []
            URL = 'https://tradeogre.com/api/v1/markets'
            req = requests.get(url = URL)
            markets = req.json()
            for item in markets:
                for pair in item.keys():
                    tradingPairs.append(pair)
            return tradingPairs
        except:
            pass
        
    def getCoin(selected):
        try:
            pair = str(selected).split('-')
            main = str(pair[0])
            site = 'https://tradeogre.com/api/v1/ticker/' + selected
            r = requests.get(url = site)
            data = r.json()
            bid = (data['bid'])
            ask = (data['ask'])
            last = (data['price'])
            values = main, bid, ask, last
            return values
        except:
            pass
