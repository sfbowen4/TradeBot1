import TradingLogic
import DataFromTD
import pandas
import datetime
import TradeAnalytics
import csv
import time

def Portfolio():
    TickerList = []
    for Ticker in TradingLogic.MasterDict['TickerList']:
        try:
            if TradingLogic.MasterDict['Data'][Ticker]['Position'] == True:
                TickerList.append(Ticker)
            else:
                None
        except:
            None
    df = pandas.DataFrame(TickerList)
    df.to_csv('Portfolio.csv', index=False, header=False)

Portfolio()

def Trade():
    for Ticker in TradingLogic.MasterDict['TickerList']:
        if TradingLogic.MasterDict['Data'][Ticker]['Position'] == False:
            #Not in portfolio
            if TradingLogic.MasterDict['Data'][Ticker]['CurrentPrice'] < (TradingLogic.MasterDict['Data'][Ticker]['DayMovingAverage'] * .995):
                Buy(Ticker)
            else:
                None
        elif TradingLogic.MasterDict['Data'][Ticker]['Position'] == True:
            #In portfolio
            if TradingLogic.MasterDict['Data'][Ticker]['CurrentPrice'] > (TradingLogic.MasterDict['Data'][Ticker]['DayMovingAverage'] * 1.02) or TradingLogic.MasterDict['Data'][Ticker]['CurrentPrice'] < (TradingLogic.MasterDict['Data'][Ticker]['LastBuy'] * .98):
                Sell(Ticker)
            else:
                None

def Buy(Ticker):
    Price = DataFromTD.QuickPrice(Ticker)
    trade = {'Type': 'Buy', 'Security': Ticker, 'Price': Price, 'Time': datetime.datetime.now(), 'DayMovingAverage': TradingLogic.MasterDict['Data'][Ticker]['DayMovingAverage']}
    TradingLogic.MasterDict['Data'][Ticker]['LastBuy'] = Price
    with open('Trades.csv', "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Type','Security','Price','Time','DayMovingAverage'])
        writer.writerow(trade)
    TradingLogic.MasterDict['Data'][Ticker]['Position'] = True
    Portfolio()

def Sell(Ticker):
    Price = DataFromTD.QuickPrice(Ticker)
    trade = {'Type': 'Sell', 'Security': Ticker, 'Price': Price, 'Time': datetime.datetime.now(), 'DayMovingAverage': TradingLogic.MasterDict['Data'][Ticker]['DayMovingAverage']}
    with open('Trades.csv', "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Type','Security','Price','Time','DayMovingAverage'])
        writer.writerow(trade)
    TradingLogic.MasterDict['Data'][Ticker]['Position'] = False
    Portfolio()

def SellAll():
    for Ticker in TradingLogic.MasterDict['TickerList']:
        try:
            if TradingLogic.MasterDict['Data'][Ticker]['Position'] == True:
                Sell(Ticker)
            else:
                None
        except:
            Portfolio()
            time.sleep(60)
            SellAll()