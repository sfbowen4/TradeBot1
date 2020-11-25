import csv

def ProfProb():
    SortedOrders = {}
    Tickers = set([])
    P = 0
    L = 0

    #Parse CSV spreadsheet
    with open('Trades.csv', newline='') as f:
        Reader = csv.reader(f)
        Data = list(Reader)

    #Remove repeated tickers
    for Order in Data:
        Tickers.add(Order[1])

    #Sort Buy/Sell prices into manageable dicts 
    for Ticker in Tickers:
        SortedOrders[Ticker] = {}
        SortedOrders[Ticker]['Buy'] = []
        SortedOrders[Ticker]['Sell'] = []
        for Order in Data:
            if Order[1] == Ticker:
                if Order[0] == 'Buy':
                    SortedOrders[Ticker]['Buy'].append(float(Order[2]))
                elif Order[0] == 'Sell':
                    SortedOrders[Ticker]['Sell'].append(float(Order[2]))
            else:
                None

    #Tally the profitable trades
    for Ticker in SortedOrders:
        for x in range(len(SortedOrders[Ticker]['Buy'])):
            try:
                if SortedOrders[Ticker]['Sell'][x] - SortedOrders[Ticker]['Buy'][x] > 0:
                    P += 1
                elif SortedOrders[Ticker]['Sell'][x] - SortedOrders[Ticker]['Buy'][x] <= 0:
                    L += 1
            except:
                None

    #percent profitability
    try:
        ProfProb = "Bot is currently {}% profitable.".format(int(P/(P+L) * 100))
    except:
        ProfProb = "No closed trades."
        
    return ProfProb


def Profits():
    SortedOrders = {}
    Tickers = set([])
    Profits = []
    FormattedProfits = []
    AverageProfit = 0

    #Parse CSV spreadsheet
    with open('Trades.csv', newline='') as f:
        Reader = csv.reader(f)
        Data = list(Reader)

    #Remove repeated tickers
    for Order in Data:
        Tickers.add(Order[1])

    #Sort Buy/Sell prices into manageable dict 
    for Ticker in Tickers:
        SortedOrders[Ticker] = {}
        SortedOrders[Ticker]['Buy'] = []
        SortedOrders[Ticker]['Sell'] = []
        for Order in Data:
            if Order[1] == Ticker:
                if Order[0] == 'Buy':
                    SortedOrders[Ticker]['Buy'].append(float(Order[2]))
                elif Order[0] == 'Sell':
                    SortedOrders[Ticker]['Sell'].append(float(Order[2]))
            else:
                None

    #Tally the profitable trades
    for Ticker in SortedOrders:
        for x in range(len(SortedOrders[Ticker]['Buy'])):
            try:
                Profits.append((SortedOrders[Ticker]['Sell'][x] - SortedOrders[Ticker]['Buy'][x]) / SortedOrders[Ticker]['Buy'][x])
            except:
                None

    for x in Profits:
        FormattedProfits.append("{}%".format(round(x,4)*100))

    for x in Profits:
        AverageProfit += x
    try:
        AverageProfit /= len(Profits)
        return("{}%".format(round(AverageProfit,4)*100))
    except:
        return "No closed trades."

if __name__ == '__main__':
    print(ProfProb())
    print(Profits())