import backtrader as bt
import pandas as pd
import itertools
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Define Trading Strategy
class MyStrategy(bt.Strategy):
    params = ("short_window", 40), ("long_window", 100)

    def __init__(self):
        self.short_mavg = bt.indicators.SimpleMovingAverage(self.datas[0].close, period=self.params.short_window)
        self.long_mavg = bt.indicators.SimpleMovingAverage(self.datas[0].close, period=self.params.long_window)

    def next(self):
        if self.short_mavg[0] > self.long_mavg[0] and not self.position:
            self.buy()
        elif self.short_mavg[0] < self.long_mavg[0] and self.position:
            self.sell()

# Function to Run a Single Backtest
def run_backtest(short_window=40, long_window=100, data_file="data/aapl_data.csv", plot_results=False):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy, short_window=short_window, long_window=long_window)

    try:
        # Load and clean data before passing to Backtrader
        df = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        df.dropna(inplace=True)

        # Ensure all values are numeric
        numeric_cols = ["Open", "High", "Low", "Close", "Volume"]
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
        df.dropna(inplace=True)

        # Convert DataFrame to Backtrader format
        data = bt.feeds.PandasData(dataname=df)
        cerebro.adddata(data)
    except FileNotFoundError:
        print(f"🚨 ERROR: Data file {data_file} not found!")
        return None
    
    cerebro.broker.set_cash(10000)
    cerebro.broker.setcommission(commission=0.001)

    # Add analyzers for performance metrics
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
    cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")

    results = cerebro.run()
    strat = results[0]
    
    if plot_results:
        cerebro.plot()
    
    return {
        "final_value": cerebro.broker.getvalue(),
        "sharpe_ratio": strat.analyzers.sharpe.get_analysis().get("sharperatio", None),
        "max_drawdown": strat.analyzers.drawdown.get_analysis()["max"]["drawdown"],
        "total_return": strat.analyzers.returns.get_analysis()["rtot"]
    }

# Function to Optimize Parameters
def optimize_parameters():
    short_windows = [5, 10, 20, 40, 60]
    long_windows = [50, 100, 150, 200]

    best_params = None
    best_performance = float("-inf")
    results = []

    os.makedirs("results", exist_ok=True)

    for short_window, long_window in itertools.product(short_windows, long_windows):
        print(f"🔍 Testing Short: {short_window}, Long: {long_window}...")
        result = run_backtest(short_window, long_window, plot_results=False)  # Disable plotting during optimization
        if result:
            results.append({
                "short_window": short_window,
                "long_window": long_window,
                "final_value": result["final_value"],
                "sharpe_ratio": result["sharpe_ratio"],
                "max_drawdown": result["max_drawdown"],
                "total_return": result["total_return"]
            })

    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv("results/optimization_results.csv", index=False)
    print("📊 Optimization results saved to `results/optimization_results.csv`")

if __name__ == "__main__":
    optimize_parameters()