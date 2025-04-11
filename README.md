# Strategic Reasoning for Stock Market Systems

**Author:** James Taylor  
**Supervisor:** Dr. Julian Gutierrez  
**Course:** BSc Computer Science – University of Sussex  
**Year:** 2024–2025  

## Project Overview

This project will explore differnet algorithmic trading strategies using historical stock market data. This implementation will also implemente machine learning. The systems design collects and cleans data, analysis trading strategies, parameter optimiation, backtesting for performance metrics and displays visuale results. The project also has a dashboard to provide users interaction a prediction.

Key areas include the following:
- Moving Average Crossover strategies (enhanced with ATR and Bollinger Bands)
- RSI-based trading systems
- Linear Regression-based stock price prediction
- Strategy performance visualization and parameter optimization

## Features

- **Data Collection & Cleaning:** Downloads data from Yahoo Finance, this will ensure accuracy.
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

The historical stock data is being downloaded from yahoo finance using `yfinance`.

This data is cleaned and then saved to the data folder as a csv.

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