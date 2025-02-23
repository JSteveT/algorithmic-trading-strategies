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

def rsi_strategy(data, period=14, overbought=70, oversold=30):
    # Calculate price differences
    delta = data['Close'].diff()
    
    # Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Calculate average gain and loss over the specified period
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    
    # Replace zeros in avg_loss to avoid division by zero
    avg_loss = avg_loss.replace(0, 1e-10)
    
    # Calculate Relative Strength (RS) and then RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    # For the first 'period' days, fill NaN values with a neutral RSI value (50)
    rsi = rsi.fillna(50)
    
    # Build signals DataFrame
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data['Close']
    signals['RSI'] = rsi
    # Generate trading signals: buy when RSI < oversold, sell when RSI > overbought
    signals['signal'] = np.where(rsi < oversold, 1, np.where(rsi > overbought, -1, 0))
    signals['positions'] = signals['signal'].diff()
    
    return signals

if __name__ == '__main__':
    # Read CSV while skipping extra header rows and set column names
    data = pd.read_csv(
        "data/aapl_data.csv",
        skiprows=3,              # Skip the extra header rows
        header=None,             # No header in the remaining rows
        names=["Date", "Close", "High", "Low", "Open", "Volume"],
        parse_dates=["Date"],
        index_col="Date"
    )
    
    # Test the moving average strategy and print the first few rows of signals
    signals = moving_average_crossover(data)
    print(signals.head())
