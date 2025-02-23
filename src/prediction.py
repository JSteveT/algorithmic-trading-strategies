import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def predict_future_price(data, window_size=5):
    """
    Predict the next day's closing price using a simple sliding-window Linear Regression.
    
    Parameters:
      data (pd.DataFrame): Historical stock data with a 'Close' column.
      window_size (int): Number of past days used as features.
    
    Returns:
      float or None: Predicted next closing price, or None if there's not enough data.
    """
    # Ensure we have more than window_size rows
    if len(data) <= window_size:
        return None

    # Get the closing prices; if it's 2D, flatten it.
    prices = data['Close'].values
    if prices.ndim > 1:
        prices = prices.flatten()
    
    X, y = [], []
    
    # Build the sliding window samples
    for i in range(len(prices) - window_size):
        # Extract a sample window and flatten to ensure 1D shape
        x = prices[i:i+window_size]
        if x.ndim > 1:
            x = x.flatten()
        X.append(x)
        y.append(prices[i+window_size])
    
    if len(X) == 0:
        return None

    X = np.array(X)
    y = np.array(y)
    
    # Train the Linear Regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Prepare the last window for prediction
    last_window = prices[-window_size:]
    if last_window.ndim > 1:
        last_window = last_window.flatten()
    last_window = last_window.reshape(1, -1)
    
    predicted_price = model.predict(last_window)
    return predicted_price[0]

# Optional testing code
if __name__ == '__main__':
    data = pd.read_csv(
        "data/aapl_data.csv",
        skiprows=3,
        header=None,
        names=["Date", "Close", "High", "Low", "Open", "Volume"],
        parse_dates=["Date"],
        index_col="Date"
    )
    prediction = predict_future_price(data)
    if prediction is not None:
        print(f"Predicted next closing price: ${prediction:.2f}")
    else:
        print("Not enough data to make a prediction.")
