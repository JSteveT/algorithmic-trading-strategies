import backtrader as bt
import numpy as np

class MovingAverageCrossover(bt.Strategy):
    params = (
        ("short_window", 40),
        ("long_window", 100),
        ("atr_period", 14),
        ("risk_factor", 1.5),
    )

    def __init__(self):
        self.short_mavg = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_window)
        self.long_mavg = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_window)
        self.atr = bt.indicators.ATR(self.data, period=self.params.atr_period)

    def next(self):
        if self.short_mavg[0] > self.long_mavg[0] and not self.position:
            self.buy()
        elif self.short_mavg[0] < self.long_mavg[0] and self.position:
            self.sell()

class RSIStrategy(bt.Strategy):
    params = (
        ("rsi_period", 14),
        ("overbought", 70),
        ("oversold", 30),
        ("sma_period", 50),
        ("atr_period", 14),
        ("risk_factor", 1.5),
        ("take_profit_factor", 2)
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.params.rsi_period)
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_period)
        self.atr = bt.indicators.ATR(self.data, period=self.params.atr_period)
        self.order = None
        self.entry_price = None

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.rsi[0] < self.params.oversold and self.data.close[0] > self.sma[0]:
                atr = self.atr[0]
                stop_price = self.data.close[0] - (self.params.risk_factor * atr)
                limit_price = self.data.close[0] + (self.params.take_profit_factor * atr)
                self.order = self.buy()
                self.entry_price = self.data.close[0]

        elif self.position:
            atr = self.atr[0]
            current_price = self.data.close[0]

            if current_price < (self.entry_price - (self.params.risk_factor * atr)):
                self.close()
                self.order = None

            elif current_price > (self.entry_price + (self.params.take_profit_factor * atr)):
                self.close()
                self.order = None

            elif self.rsi[0] > 50:
                self.close()
                self.order = None
