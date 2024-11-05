import pandas as pd
import numpy as np

def moving_average_crossover(data, short_window=40, long_window=100):
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data['Close']
    signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    signals['signal'] = 0
    signals['signal'][short_window:] = np.where(
        signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1, 0
    )
    signals['positions'] = signals['signal'].diff()
    return signals

data = pd.read_csv("data/aapl_data.csv", index_col="Date", parse_dates=True)
signals = moving_average_crossover(data)
print(signals.head())