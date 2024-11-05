import streamlit as st
import pandas as pd
from strategy import moving_average_crossover

st.title("Stock Market Trading Strategy")

ticker = st.text_input("Enter Stock Ticker", "aapl")
data = pd.read_csv(f"data/aapl_data.csv", index_col="Date", parse_dates=True)
signals = moving_average_crossover(data)
st.line_chart(signals[['price', 'short_mavg', 'long_mavg']])