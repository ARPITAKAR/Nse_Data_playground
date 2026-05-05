# gold-silver-arima-trading
Statistical arbitrage strategy using ARIMA for gold–silver mean reversion.
# Gold–Silver Relative Value Trading (ARIMA)

A quantitative trading project implementing a **mean reversion strategy** on the gold–silver spread using **ARIMA time-series modeling**.

## 📌 Overview
This project models the price relationship between gold and silver to identify trading opportunities based on deviations from their historical spread.

## ⚙️ Approach
- Construct spread between gold and silver prices  
- Fit ARIMA model on spread  
- Forecast expected values  
- Generate trading signals based on deviations  

## 📊 Features
- ARIMA-based forecasting  
- Mean reversion strategy  
- Backtesting with performance metrics  

## 🛠️ Tech Stack
Python, pandas, numpy, statsmodels

## 🚀 Usage
```bash
pip install -r requirements.txt
jupyter notebook
