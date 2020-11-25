import DataFromTD

MasterDict = {'TickerList': []}

#Initialize master dictionary with all information required to trade
def BuildMasterDict():
    global MasterDict
    Movers = DataFromTD.UpwardMovers()
    CurrentPrices = DataFromTD.CurrentPrice(Movers)
    MasterDict['TickerList'] = Movers
    MasterDict['Data'] = {}
    for Ticker in MasterDict['TickerList']:
        DayMovingAverage = DataFromTD.DayMovingAverage(Ticker)
        MasterDict['Data'][Ticker] = {'CurrentPrice': CurrentPrices[Ticker], 'DayMovingAverage': DayMovingAverage[0], 'Position': False, 'PriceHistory': DayMovingAverage[1], 'LastBuy': 0}
        
#Refresh master dictionary with new values while maintaining portfolio
def RefreshMasterDict():
    global MasterDict
    Movers = DataFromTD.UpwardMovers()
    CurrentPrices = DataFromTD.CurrentPrice(Movers)
    #Add new Tickers to list
    for Ticker in Movers:
        if Ticker in MasterDict['TickerList']:
            None
        else:
            DayMovingAverage = DataFromTD.DayMovingAverage(Ticker)
            MasterDict['Data'][Ticker] = {'CurrentPrice': CurrentPrices[Ticker], 'DayMovingAverage': DayMovingAverage[0], 'Position': False, 'PriceHistory': DayMovingAverage[1], 'LastBuy': 0}
            MasterDict['TickerList'].append(Ticker)
            MasterDict['Data'][Ticker]['CurrentPrice'] = CurrentPrices[Ticker]
    CurrentPrices = DataFromTD.CurrentPrice(MasterDict['TickerList'])
    for Ticker in MasterDict['TickerList']:
        MasterDict['Data'][Ticker]['CurrentPrice'] = CurrentPrices[Ticker]
        MasterDict['Data'][Ticker]['PriceHistory'].append(CurrentPrices[Ticker])