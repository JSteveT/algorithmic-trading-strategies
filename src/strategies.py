import pandas as pd
import numpy as np

def moving_average_crossover(data, short_window=40, long_window=100, atr_period=14, risk_pct=0.02):
    """
    Enhanced Moving Average Crossover strategy with:
    - Bollinger Bands as a volatility filter
    - ATR-based stop-loss & take-profit
    - Dynamic position sizing
    """
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data['Close']
    
    # Moving Averages
    signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    
    # Ensure we have enough data before computing Bollinger Bands
    if len(signals) >= short_window:
        # Ensure std_dev is a Series (not DataFrame)
        std_dev = data['Close'].rolling(window=short_window, min_periods=1).std()

        # Assign correctly
        signals['bollinger_upper'] = signals['short_mavg'] + (2 * std_dev.squeeze())
        signals['bollinger_lower'] = signals['short_mavg'] - (2 * std_dev.squeeze())

    else:
        signals['bollinger_upper'] = np.nan
        signals['bollinger_lower'] = np.nan
    
    # ATR Calculation
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    signals['ATR'] = tr.rolling(atr_period).mean()
    
    # Drop initial NaN rows where ATR is not calculated yet
    signals.dropna(subset=['ATR'], inplace=True)
    
    # Ensure all series are aligned by reindexing
    signals = signals.reindex(data.index).dropna()
    
    # Trading Signal (1 = Buy, -1 = Sell, 0 = Hold)
    signals['signal'] = 0
    signals.loc[(signals['short_mavg'] > signals['long_mavg']) & (signals['price'] > signals['bollinger_lower']), 'signal'] = 1
    signals.loc[(signals['short_mavg'] < signals['long_mavg']) & (signals['price'] < signals['bollinger_upper']), 'signal'] = -1
    
    # Stop-Loss & Take-Profit (ATR-based)
    signals['stop_loss'] = np.where(signals['signal'] == 1, signals['price'] - (1.5 * signals['ATR']), np.nan)
    signals['take_profit'] = np.where(signals['signal'] == 1, signals['price'] + (2 * signals['ATR']), np.nan)
    
    # Position Sizing: Ensure ATR is available
    initial_capital = 10000  # Example starting capital
    signals['position_size'] = np.where(signals['ATR'].notna(), (risk_pct * initial_capital) / (2 * signals['ATR']), np.nan)
    
    # Track changes in positions
    signals['positions'] = signals['signal'].diff()
    
    return signals

def rsi_strategy(data, period=14, overbought=70, oversold=30):
    """
    Relative Strength Index (RSI) Strategy
    """
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    avg_loss = avg_loss.replace(0, 1e-10)  # Avoid division by zero
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    rsi = rsi.fillna(50)
    
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data['Close']
    signals['RSI'] = rsi
    
    # Generate trading signals: buy when RSI < oversold, sell when RSI > overbought
    signals['signal'] = np.where(rsi < oversold, 1, np.where(rsi > overbought, -1, 0))
    signals['positions'] = signals['signal'].diff()
    
    return signals

if __name__ == '__main__':
    data = pd.read_csv("data/aapl_data.csv", parse_dates=["Date"], index_col="Date")
    
    # Ensure numeric data
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    data.dropna(inplace=True)
    
    # Test moving average strategy
    signals = moving_average_crossover(data)
    print(signals.head())