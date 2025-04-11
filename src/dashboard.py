import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prediction import predict_future_price
from backtesting import run_backtest, MovingAverageCrossover, RSIStrategy

# Load Data with Error Handling
def load_data():
    try:
        data = pd.read_csv("data/aapl_data.csv", parse_dates=["Date"], index_col="Date")
        # Ensure numeric values only
        data = data.apply(pd.to_numeric, errors='coerce')
        data.dropna(inplace=True)
        return data
    except FileNotFoundError:
        st.error("Data file not found! Please run the data collection and enhancement scripts before launching the dashboard.")
        return None

data = load_data()
if data is None:
    st.stop()

st.title("Trading Strategy Dashboard")

st.subheader("Historical Stock Data")
st.line_chart(data['Close'], height=500)

st.subheader("Stock Price Prediction")
try:
    predicted_price = predict_future_price(data)
    if predicted_price:
        st.write(f"Predicted next closing price: **${predicted_price:.2f}**")
    else:
        st.write("Not enough data to make a prediction.")
except Exception as e:
    st.error(f"Error in prediction: {e}")

st.subheader("Strategy Performance")
strategy = st.selectbox("Select Strategy", ["Moving Average Crossover", "RSI Strategy"])

if strategy == "Moving Average Crossover":
    result = run_backtest(MovingAverageCrossover, short_window=40, long_window=100)
else:
    result = run_backtest(RSIStrategy)

st.write(f"Final Portfolio Value: **${result['final_value']:.2f}**")
st.write(f"Sharpe Ratio: **{result['sharpe_ratio']:.2f}**")
st.write(f"Max Drawdown: **{result['max_drawdown']:.2f}%**")
st.write(f"Total Return: **{result['total_return']:.2%}**")

st.subheader("Optimization Results")
try:
    results_df = pd.read_csv("results/optimization_results.csv")
    st.dataframe(results_df)

    st.subheader("Optimization Heatmap")
    pivot_sharpe = results_df.pivot(index="long_window", columns="short_window", values="sharpe_ratio")
    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot_sharpe, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
    st.pyplot(plt)
except FileNotFoundError:
    st.error("Optimization results file not found! Please run the optimization script before viewing results.")
