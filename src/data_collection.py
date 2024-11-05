import yfinance as yf
import pandas as pd

def fetch_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data.dropna(inplace=True)
    return data

# Fetch data and save to CSV
data = fetch_data("AAPL", "2020-01-01", "2023-01-01")
data.to_csv("data/aapl_data.csv")