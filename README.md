# Strategic Reasoning for Stock Market Systems

**Author:** James Taylor  
**Supervisor:** Dr. Julian Gutierrez  
**Course:** BSc Computer Science – University of Sussex  
**Year:** 2024–2025  

## Project Overview

This project explores algorithmic trading strategies using historical stock market data and machine learning. The system is designed to collect and clean stock data, implement trading strategies, optimize their parameters, backtest their performance, and visualize results. It also includes a dashboard for user interaction and prediction.

Key focus areas include:
- Moving Average Crossover strategies (enhanced with ATR and Bollinger Bands)
- RSI-based trading systems
- Linear Regression-based stock price prediction
- Strategy performance visualization and parameter optimization

## Features

- **Data Collection & Cleaning:** Pulls data from Yahoo Finance, ensures accuracy.
- **Predictive Modeling:** Linear Regression to predict next-day closing prices.
- **Strategies Implemented:**
  - Moving Average Crossover with Bollinger Bands, ATR-based stop-loss/take-profit.
  - RSI-based strategy.
- **Backtesting Framework:** Using `Backtrader` with Sharpe Ratio, Drawdown, and Return analysis.
- **Optimization Module:** Exhaustive parameter tuning with heatmap output.
- **Streamlit Dashboard:** Interactive interface showing predictions, backtests, and optimization visuals.

## Project Structure

```
.
├── src/
│   ├── data_collection.py          
│   ├── data_enhancements.py        
│   ├── prediction.py               
│   ├── strategies.py               
│   ├── backtesting.py              
│   ├── optimization.py             
│   ├── dashboard.py                
├── data/                           
├── results/                        
└── README.md                       
```

## Getting Started

### 1. **Set up your environment**
```bash
pip install -r requirements.txt
```

Recommended packages:
- `yfinance`
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `backtrader`
- `scikit-learn`
- `streamlit`

### 2. **Run data collection**
```bash
python data_collection.py
```

### 3. **Run backtesting or optimization**
```bash
python backtesting.py
# or
python optimization.py
```

### 4. **Launch dashboard**
```bash
streamlit run dashboard.py
```

## Data

All historical stock data is pulled from Yahoo Finance using `yfinance`. Example ticker: `AAPL`.

Cleaned data is saved in the `data/` folder as CSV files (e.g., `aapl_data.csv`).

## Testing

Testing is mainly conducted via:
- Historical backtests using `Backtrader`.
- Parameter optimization sweeps with Sharpe Ratio analysis.
- Optional user testing for UI/UX (see compliance form in Appendix).

## Ethics & Compliance

All user testing adheres to the **BCS Code of Conduct** and **GDPR** guidelines.  
Please refer to the signed User Testing Compliance Form in the report appendix.

## References

- Yahoo Finance API
- Investopedia
- QuantStart
- Towards Data Science
- Scikit-learn documentation
- Backtrader documentation