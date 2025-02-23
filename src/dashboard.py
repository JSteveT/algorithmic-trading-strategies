import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
from strategies import moving_average_crossover, rsi_strategy
from prediction import predict_future_price

def get_signals(data, strategy):
    if strategy == "Moving Average":
        return moving_average_crossover(data)
    elif strategy == "RSI":
        return rsi_strategy(data)
    else:
        return None

st.title("Stock Market Trading Strategy")

# Stock ticker input
ticker = st.text_input("Enter Stock Ticker", "AAPL")

# Checkbox to decide if a custom date range should be used
use_custom_date = st.checkbox("Use custom date range?", value=False)

if use_custom_date:
    # User can specify start and end dates if they choose
    start_date = st.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("today"))
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
else:
    # Default to fetching all available data
    start_date_str = "1900-01-01"
    end_date_str = datetime.today().strftime("%Y-%m-%d")

# Strategy selector
strategy_choice = st.selectbox("Select Strategy", ["Moving Average", "RSI"])

if st.button("Fetch Data"):
    data = yf.download(ticker, start=start_date_str, end=end_date_str, progress=False)
    if data.empty:
        st.error(f"No data found for ticker: {ticker}")
    else:
        data.index.name = "Date"  # Ensure the index is named correctly
        signals = get_signals(data, strategy_choice)
        
        st.subheader("Price Chart")
        st.line_chart(signals[['price']])
        
        if strategy_choice == "Moving Average":
            st.subheader("Moving Averages")
            st.line_chart(signals[['short_mavg', 'long_mavg']])
        elif strategy_choice == "RSI":
            st.subheader("RSI")
            st.line_chart(signals[['RSI']])
        
        st.subheader("Future Price Prediction")
        predicted_price = predict_future_price(data)
        if predicted_price is not None:
            st.write(f"Predicted next closing price: **${predicted_price:.2f}**")
        else:
            st.error("Not enough data to make a prediction.")
