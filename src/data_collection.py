import yfinance as yf
import pandas as pd

def fetch_data(ticker, start_date, end_date):
    
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)

    data.reset_index(inplace=True)

    data = data[["Date", "Open", "High", "Low", "Close", "Volume"]]

    data[["Open", "High", "Low", "Close", "Volume"]] = data[["Open", "High", "Low", "Close", "Volume"]].apply(pd.to_numeric, errors="coerce")

    data = data[data["Date"].notna()]
    data = data.iloc[1:]

    output_file = f"data/{ticker.lower()}_data.csv"
    data.to_csv(output_file, index=False)

    print(f"Clean data saved to {output_file}")

fetch_data("AAPL", "2020-01-01", "2023-01-01")
