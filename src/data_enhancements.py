import yfinance as yf
import pandas as pd
import os

def fetch_yahoo_data(ticker, start_date="2020-01-01", end_date="2023-01-01"):
    print(f"Fetching data for {ticker} from Yahoo Finance...")

    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)

    data.dropna(inplace=True)

    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{ticker.lower()}_yahoo.csv")
    data.to_csv(output_file, index=True, float_format="%.6f")

    print(f"Data saved successfully to {output_file}")
    return data

ticker = "AAPL"
data = fetch_yahoo_data(ticker)

print(data.head())
