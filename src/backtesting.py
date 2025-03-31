import backtrader as bt
import pandas as pd
from strategies import MovingAverageCrossover, RSIStrategy

def run_backtest(strategy, short_window=None, long_window=None, data_file="data/aapl_data.csv", cash=10000, commission=0.001):
    cerebro = bt.Cerebro()

    if strategy == MovingAverageCrossover:
        cerebro.addstrategy(strategy, short_window=short_window, long_window=long_window)
    else:
        cerebro.addstrategy(strategy)

    data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
    data = data.apply(pd.to_numeric, errors="coerce").dropna()

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

def compare_strategies():
    print("\n🔍 Running Comparative Backtests\n" + "-" * 40)

    print("\n📈 MA Crossover (40/100):")
    ma_default = run_backtest(MovingAverageCrossover, short_window=40, long_window=100)
    for k, v in ma_default.items():
        print(f"{k.replace('_', ' ').title()}: {v:.4f}" if isinstance(v, float) else f"{k.title()}: {v}")

    print("\n🏆 MA Crossover (Optimised 20/100):")
    ma_opt = run_backtest(MovingAverageCrossover, short_window=20, long_window=100)
    for k, v in ma_opt.items():
        print(f"{k.replace('_', ' ').title()}: {v:.4f}" if isinstance(v, float) else f"{k.title()}: {v}")

    print("\n📉 RSI Strategy:")
    rsi = run_backtest(RSIStrategy)
    for k, v in rsi.items():
        print(f"{k.replace('_', ' ').title()}: {v:.4f}" if isinstance(v, float) else f"{k.title()}: {v}")

if __name__ == "__main__":
    compare_strategies()