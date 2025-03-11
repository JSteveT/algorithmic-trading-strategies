import yfinance as yf
import pandas as pd
import os

def fetch_yahoo_data(ticker, start_date="2020-01-01", end_date="2023-01-01"):
    """Fetch stock data from Yahoo Finance and save it as a CSV."""
    print(f"Fetching data for {ticker} from Yahoo Finance...")

    # Download stock data
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)

    # Drop missing values
    data.dropna(inplace=True)

    # Ensure the 'data' directory exists
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    # Save to CSV
    output_file = os.path.join(output_dir, f"{ticker.lower()}_yahoo.csv")
    data.to_csv(output_file, index=True, float_format="%.6f")

    print(f"Data saved successfully to {output_file}")
    return data

# Example usage
ticker = "AAPL"
data = fetch_yahoo_data(ticker)

# Display first few rows to confirm data retrieval
print(data.head())
