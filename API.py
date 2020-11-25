from fastapi import FastAPI
import TradeAnalytics
import uvicorn
import csv

def Master():
        with open("MasterData.txt") as file:
                return file.read()

app = FastAPI()

@app.get("/analytics")
def read_root():
        ProfProb = TradeAnalytics.ProfProb()
        Profits = TradeAnalytics.Profits()
        return {'ProfProb': ProfProb, 'Profits': Profits}

@app.get("/portfolio")
def read():
        with open('Portfolio.csv', newline='') as f:
                TickerList = []
                Reader = csv.reader(f)
                Data = list(Reader)
                for item in range(len(Data)):
                        TickerList.append(Data[item][0])
        return {'TickerList': TickerList}

def Start():
        uvicorn.run(app, host="192.168.1.49")

if __name__ == "__main__":
        Start()