import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def predict_future_price(data, window_size=5):

    if len(data) <= window_size:
        return None

    prices = data['Close'].values
    if prices.ndim > 1:
        prices = prices.flatten()
    
    X, y = [], []
    
    for i in range(len(prices) - window_size):
        x = prices[i:i+window_size]
        if x.ndim > 1:
            x = x.flatten()
        X.append(x)
        y.append(prices[i+window_size])
    
    if len(X) == 0:
        return None

    X = np.array(X)
    y = np.array(y)
    
    model = LinearRegression()
    model.fit(X, y)
    
    last_window = prices[-window_size:]
    if last_window.ndim > 1:
        last_window = last_window.flatten()
    last_window = last_window.reshape(1, -1)
    
    predicted_price = model.predict(last_window)
    return predicted_price[0]

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
