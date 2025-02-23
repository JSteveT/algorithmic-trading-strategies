import pandas as pd
import numpy as np

def fetch_alpha_vantage_data(ticker, api_key, outputsize='full'):
    # ... (code as provided)
    return df

def compute_rsi(df, period=14):
    # ... (code as provided)
    return df

def preprocess_data(df):
    # ... (code as provided)
    return df

if __name__ == '__main__':
    # Example usage
    api_key = "YOUR_ALPHA_VANTAGE_API_KEY"
    ticker = "AAPL"
    data = fetch_alpha_vantage_data(ticker, api_key)
    enhanced_data = preprocess_data(data)
    print(enhanced_data.head())
