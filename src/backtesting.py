import backtrader as bt
import pandas as pd

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data, period=15)

    def next(self):
        if self.data.close[0] > self.sma[0]:
            self.buy()
        elif self.data.close[0] < self.sma[0]:
            self.sell()

# Initialize Cerebro engine
cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)

# Load data from CSV
data = bt.feeds.YahooFinanceCSVData(dataname="data/aapl_data.csv")

# Add the data to Cerebro
cerebro.adddata(data)

# Run the backtest
cerebro.run()
cerebro.plot()
