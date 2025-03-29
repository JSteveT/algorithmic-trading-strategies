import backtrader as bt
import pandas as pd
import itertools
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ✅ Moving Average Crossover Strategy with ATR-based exits
class MovingAverageCrossover(bt.Strategy):
    params = (("short_window", 10), ("long_window", 100), ("atr_period", 14), ("risk_factor", 1.5))

    def __init__(self):
        self.short_mavg = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_window)
        self.long_mavg = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_window)
        self.atr = bt.indicators.ATR(self.data, period=self.params.atr_period)

    def next(self):
        if self.short_mavg[0] > self.long_mavg[0] and not self.position:
            atr_value = self.atr[0] * self.params.risk_factor
            self.buy(exectype=bt.Order.Stop, price=self.data.close[0] - atr_value)
        elif self.short_mavg[0] < self.long_mavg[0] and self.position:
            self.sell()

# ✅ RSI-Based Strategy for Comparison
class RSIStrategy(bt.Strategy):
    params = (("rsi_period", 14), ("overbought", 70), ("oversold", 30))

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.params.rsi_period)

    def next(self):
        if self.rsi[0] < self.params.oversold and not self.position:
            self.buy()
        elif self.rsi[0] > self.params.overbought and self.position:
            self.sell()

# ✅ Function to Run a Single Backtest
def run_backtest(strategy, short_window=None, long_window=None, data_file="data/aapl_data.csv", cash=10000, commission=0.001):
    cerebro = bt.Cerebro()

    # Ensure strategy is passed correctly
    if strategy == MovingAverageCrossover:
        cerebro.addstrategy(strategy, short_window=short_window, long_window=long_window)
    else:
        cerebro.addstrategy(strategy)  # Run RSI without extra parameters

    try:
        data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
    except FileNotFoundError:
        print(f"🚨 ERROR: Data file {data_file} not found!")
        return None

    # Ensure all values are numeric and drop NaNs
    data = data.apply(pd.to_numeric, errors="coerce").dropna()

    if data.empty:
        print("🚨 ERROR: Data is empty after processing!")
        return None

    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(data_feed)

    cerebro.broker.set_cash(cash)
    cerebro.broker.setcommission(commission=commission)

    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
    cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")

    results = cerebro.run()
    strat = results[0]

    return {
        "final_value": cerebro.broker.getvalue(),
        "sharpe_ratio": strat.analyzers.sharpe.get_analysis().get("sharperatio", None),
        "max_drawdown": strat.analyzers.drawdown.get_analysis()["max"]["drawdown"],
        "total_return": strat.analyzers.returns.get_analysis()["rtot"]
    }



# ✅ Function to Optimize Parameters and Save Results
def optimize_parameters():
    short_windows = [5, 10, 15, 20, 30, 40, 50, 60]  # Expanded range
    long_windows = [80, 100, 120, 150, 180, 200, 250]  # Expanded range

    best_params = None
    best_sharpe = float("-inf")
    results = []

    os.makedirs("results", exist_ok=True)

    for short_window, long_window in itertools.product(short_windows, long_windows):
        print(f"🔍 Testing Short: {short_window}, Long: {long_window}...")
        result = run_backtest(MovingAverageCrossover, short_window, long_window)
        result["short_window"] = short_window
        result["long_window"] = long_window
        results.append(result)

        if result["sharpe_ratio"] and result["sharpe_ratio"] > best_sharpe:
            best_sharpe = result["sharpe_ratio"]
            best_params = (short_window, long_window)

    print("\n🎯 **Best Parameters Found:**")
    print(f"Short Window: {best_params[0]}")
    print(f"Long Window: {best_params[1]}")
    print(f"Best Sharpe Ratio: {best_sharpe:.2f}")

    results_df = pd.DataFrame(results)
    results_df.to_csv("results/optimization_results.csv", index=False)
    print("📊 Optimization results saved to `results/optimization_results.csv`")

# ✅ Function to Visualize Optimization Results
def visualize_results():
    results_df = pd.read_csv("results/optimization_results.csv")

    # Pivot data for heatmap
    pivot_sharpe = results_df.pivot(index="long_window", columns="short_window", values="sharpe_ratio")
    pivot_return = results_df.pivot(index="long_window", columns="short_window", values="total_return")

    # Find the best Sharpe ratio location
    best_sharpe_idx = np.unravel_index(np.nanargmax(pivot_sharpe.values), pivot_sharpe.shape)
    best_sharpe_value = pivot_sharpe.values[best_sharpe_idx]
    best_sharpe_x = pivot_sharpe.columns[best_sharpe_idx[1]]
    best_sharpe_y = pivot_sharpe.index[best_sharpe_idx[0]]

    plt.figure(figsize=(12, 5))

    # Sharpe Ratio Heatmap
    plt.subplot(1, 2, 1)
    sns.heatmap(pivot_sharpe, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, cbar_kws={'label': 'Sharpe Ratio'})
    plt.scatter(best_sharpe_x, best_sharpe_y, color='yellow', s=100, edgecolors='black', label="Best Sharpe")
    plt.title("Sharpe Ratio Heatmap")
    plt.xlabel("Short Window")
    plt.ylabel("Long Window")
    plt.legend()

    # Total Return Heatmap
    plt.subplot(1, 2, 2)
    sns.heatmap(pivot_return, annot=True, fmt=".2%", cmap="viridis", linewidths=0.5, cbar_kws={'label': 'Total Return'})
    plt.title("Total Return Heatmap")
    plt.xlabel("Short Window")
    plt.ylabel("Long Window")

    plt.tight_layout()
    plt.savefig("results/optimized_visuals.png")
    plt.show()

def run_all_backtests():
    print("\n📊 Running Core Strategy Comparisons\n" + "-" * 40)

    # === MA Crossover with default parameters ===
    print("📈 Moving Average Crossover (default 40/100):")
    ma_default = run_backtest(MovingAverageCrossover, short_window=40, long_window=100)
    print(f"Final Value: ${ma_default['final_value']:.2f}")
    print(f"Sharpe Ratio: {ma_default['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {ma_default['max_drawdown']:.2f}%")
    print(f"Total Return: {ma_default['total_return']:.2%}\n")

    # === Best MA Crossover from optimisation ===
    best_params = pd.read_csv("results/optimization_results.csv")
    best_row = best_params.sort_values(by="sharpe_ratio", ascending=False).iloc[0]
    short = int(best_row["short_window"])
    long = int(best_row["long_window"])
    
    print(f"🏆 Optimised MA Crossover (Short: {short}, Long: {long}):")
    ma_optimised = run_backtest(MovingAverageCrossover, short_window=short, long_window=long)
    print(f"Final Value: ${ma_optimised['final_value']:.2f}")
    print(f"Sharpe Ratio: {ma_optimised['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {ma_optimised['max_drawdown']:.2f}%")
    print(f"Total Return: {ma_optimised['total_return']:.2%}\n")

    # === RSI Strategy ===
    print("📉 RSI Strategy (default 14/70/30):")
    rsi_results = run_backtest(RSIStrategy)
    print(f"Final Value: ${rsi_results['final_value']:.2f}")
    print(f"Sharpe Ratio: {rsi_results['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {rsi_results['max_drawdown']:.2f}%")
    print(f"Total Return: {rsi_results['total_return']:.2%}")
    
if __name__ == "__main__":
    # 🔥 Step 1: Optimise MA Parameters
    optimize_parameters()

    # 🔥 Step 2: Visualise Results
    visualize_results()

    # 🔥 Step 3: Run All Key Strategy Backtests
    run_all_backtests()
