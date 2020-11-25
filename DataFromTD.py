import requests
from Credentials import client_id, AccountNumber
import Authenticator
import datetime

#Pull the current price of the input ticker LIST
def CurrentPrice(tickers):
    prices = {}
    Formatted = '%2C'.join(tickers)
    endpoint = r"https://api.tdameritrade.com/v1/marketdata/quotes?symbol={}".format(Formatted)
    content = requests.get(url = endpoint, headers = Authenticator.AuthorizedToken)
    data = content.json()
    for symbol in data:
        prices[symbol] = data[symbol]['lastPrice']
    return prices

#Used to construct moving average for the day
def DayMovingAverage(ticker):
    periodType = 'day'
    period = '1'
    frequencyType = 'minute'
    frequency = '1'
    needExtendedHoursData = 'true'
    parameters = "periodType={}&period={}&frequencyType={}&frequency={}&needExtendedHoursData={}".format(periodType, period, frequencyType, frequency, needExtendedHoursData)
    endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/pricehistory?{}".format(ticker, parameters)
    content = requests.get(url = endpoint, headers = Authenticator.AuthorizedToken)
    data = content.json()
    total = 0
    PriceHistory = []
    for snapshot in data['candles']:
        PriceHistory.append(snapshot['close'])
        total += snapshot['close']
    total /= len(data['candles'])
    return total, PriceHistory

#Temporary until Trading is active
def QuickPrice(ticker):
    endpoint = r"https://api.tdameritrade.com/v1/marketdata/quotes?symbol={}".format(ticker)
    content = requests.get(url = endpoint, headers = Authenticator.AuthorizedToken)
    data = content.json()
    price = data[ticker]['lastPrice']
    return price

#Pull watchlist from TD account
def Watchlist():
    Tickers = []
    endpoint = r"https://api.tdameritrade.com/v1/accounts/{}/watchlists/1464486546".format(AccountNumber)
    content = requests.get(url = endpoint, headers = Authenticator.AuthorizedToken)
    data = content.json()
    for x in range(len(data['watchlistItems'])):
        Tickers.append(data['watchlistItems'][x]['instrument']['symbol'])
    return Tickers

#Pull the Current Account Value from TD
def AccountValue():
    endpoint = r"https://api.tdameritrade.com/v1/accounts"
    content = requests.get(url = endpoint, headers = Authenticator.AuthorizedToken)
    data = content.json()
    balance = data[0]['securitiesAccount']['initialBalances']['liquidationValue']
    return balance

#Pull the current cash balance from TD account
def CashBalance():
    endpoint = r"https://api.tdameritrade.com/v1/accounts"
    content = requests.get(url = endpoint, headers = Authenticator.AuthorizedToken)
    data = content.json()
    balance = data[0]['securitiesAccount']['initialBalances']['cashBalance']
    return balance

#Pull the current upward movers
def UpwardMovers():
    Markets = ['$COMPX','$DJI','$SPX.X']
    MoversRaw = []
    MoverTickers = []
    for Market in Markets:
        endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/movers?direction=up&change=percent".format(Market)
        content = requests.get(url = endpoint, headers = Authenticator.AuthorizedToken)
        data = content.json()
        MoversRaw.append(data)
    for MarketMovers in MoversRaw:
        for security in MarketMovers:
            MoverTickers.append(security['symbol'])
    return MoverTickers

#Pull symbols of current positions
def PositionSymbols():
    Positions = []
    endpoint = r"https://api.tdameritrade.com/v1/accounts/{}?fields=positions".format(AccountNumber)
    content = requests.get(url = endpoint, headers = Authenticator.AuthorizedToken)
    data = content.json()
    RawPositions = data['securitiesAccount']['positions']
    for info in RawPositions:
        Positions.append(info['instrument']['symbol'])
    return Positions

#Check if market is open
def IsMarketOpen():
    Today = datetime.datetime.today()
    Now = Today.time()
    endpoint = r"https://api.tdameritrade.com/v1/marketdata/EQUITY/hours?apikey={}&date={}".format(client_id,Today)
    content = requests.get(url = endpoint, headers = Authenticator.AuthorizedToken)
    data = content.json()
    try:
        MarketOpenToday = data['equity']['EQ']['isOpen']
    except:
        return False
    MarketStart = datetime.time(8, 30, 0, 0)
    MarketEnd =  datetime.time(15, 0, 0, 0)
    if MarketOpenToday == True:
        if MarketStart < Now < MarketEnd:
            return True
        else:
            return False
    else:
        return False
        
#Check if premarket is open
def IsPreMarketOpen():
    Today = datetime.datetime.today()
    Now = Today.time()
    endpoint = r"https://api.tdameritrade.com/v1/marketdata/EQUITY/hours?apikey={}&date={}".format(client_id,Today)
    content = requests.get(url = endpoint, headers = Authenticator.AuthorizedToken)
    data = content.json()
    try:
        MarketOpenToday = data['equity']['EQ']['isOpen']
    except:
        return False
    MarketStart = datetime.time(6, 0, 0, 0)
    MarketEnd =  datetime.time(15, 0, 0, 0)
    if MarketOpenToday == True:
        if MarketStart < Now < MarketEnd:
            return True
        else:
            return False
    else:
        return False