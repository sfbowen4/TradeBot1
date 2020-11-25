import DataFromTD
import time
import TradingLogic
import TDExecutionInterface
import Authenticator
import json
import TradeAnalytics
import os
import datetime
import pandas

Tries = 0
FirstOpen = 0

def TimeCheck():
    Today = datetime.datetime.today()
    Now = Today
    MarketStart = datetime.datetime(Today.year,Today.month,Today.day,8, 30, 0, 0)
    MarketEnd =  datetime.datetime(Today.year,Today.month,Today.day,15, 0, 0, 0)
    Buffer = datetime.timedelta(minutes=3)
    Buffer = MarketEnd - Buffer
    if MarketStart < Now < MarketEnd:
        if MarketStart < Now < Buffer:
            return True
        else:
            return False
    else:
        return False

def TrackSecurities():
    Authenticator.RefreshAuth()
    try:
        with open('MasterData.txt', 'w') as outfile:
            json.dump(TradingLogic.MasterDict, outfile)
        for x in range(25):
            if TimeCheck() == True:
                None
            else:
                TDExecutionInterface.SellAll()
                time.sleep(120)
                MarketOpen()
            TDExecutionInterface.Trade()
            time.sleep(60)
            TradingLogic.RefreshMasterDict()
    except:
        None
    print('Done')
    MarketOpen()

def MarketOpen():
    global Tries
    global FirstOpen
    try:
        while True:
            IsTheMarketOpen = DataFromTD.IsMarketOpen() 
            while IsTheMarketOpen == True:
                os.system('cls')
                print('The markets are open.')
                while FirstOpen < 1:
                    TradingLogic.BuildMasterDict()
                    FirstOpen += 1
                else:
                    None
                TrackSecurities()
            else:
                os.system('cls')
                print('Bot is currently offline.')
                time.sleep(60)
                Tries += 1
                if Tries % 20 == 0:
                    Authenticator.RefreshAuth()
                    TradingLogic.MasterDict = {}
                else:
                    None
    except:
        None

while True:
    MarketOpen()