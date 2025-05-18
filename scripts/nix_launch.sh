#!/usr/bin/env bash

echo "Entering Nix Shell..."
nix-shell --run '
  echo "Activating virtual environment..."
  source venv/bin/activate

  echo "Fetching fresh AAPL stock data..."
  python src/data_collection.py

  echo "Running strategy optimization..."
  python src/backtesting.py

  echo "Launching Streamlit dashboard..."
  streamlit run src/dashboard.py
'
