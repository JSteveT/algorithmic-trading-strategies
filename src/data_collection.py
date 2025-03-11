import yfinance as yf
import pandas as pd

def fetch_data(ticker, start_date, end_date):
    """Fetch clean stock data from Yahoo Finance and remove any extra rows."""
    
    # Download stock data
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)

    # Reset index to make 'Date' a column
    data.reset_index(inplace=True)

    # Ensure proper column selection
    data = data[["Date", "Open", "High", "Low", "Close", "Volume"]]

    # Convert to numeric (fix any text issues)
    data[["Open", "High", "Low", "Close", "Volume"]] = data[["Open", "High", "Low", "Close", "Volume"]].apply(pd.to_numeric, errors="coerce")

    # 🚀 **NEW FIX: Remove any unwanted rows**
    data = data[data["Date"].notna()]  # Ensure no NaN date rows exist
    data = data.iloc[1:]  # Remove the **first data row if it's corrupted**

    # Save cleaned file
    output_file = f"data/{ticker.lower()}_data.csv"
    data.to_csv(output_file, index=False)

    print(f"✅ Clean data saved to {output_file}")

# Fetch and save clean data
fetch_data("AAPL", "2020-01-01", "2023-01-01")
