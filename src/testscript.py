import yfinance as yf
from src.metrics import performance

data = yf.download("AAPL", period="6mo")
prices = data["Close"]

print("Cumulative Return:", performance.cumulative_return(prices))
print("Sharpe Ratio:", performance.sharpe_ratio(prices))
print("Max Drawdown:", performance.max_drawdown(prices))