import yfinance as yf
import pandas as pd
from data_enhancements import preprocess_data  # Your data cleaning/enhancement module

def fetch_data(ticker, start_date=None, end_date=None):
    # If no start and end dates are provided, fetch maximum available data.
    if start_date is None and end_date is None:
        data = yf.download(ticker, start="2020-01-01", end="2023-01-01", progress=False)
    else:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    data.dropna(inplace=True)
    # Enhance the data by adding new features and cleaning it
    data = preprocess_data(data)
    return data

# Example usage:
if __name__ == '__main__':
    # Fetch all available data for AAPL
    data = fetch_data("AAPL")
    data.to_csv("data/aapl_data.csv")
