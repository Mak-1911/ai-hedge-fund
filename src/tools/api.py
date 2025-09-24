import yfinance as yf

def get_latest_price(ticker:str) -> float:
    """Fetch the latest closing price of a stock."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        if not hist.empty:
            return round(hist["Close"].iloc[-1], 2)
        return 0.0
    except Exception as e:
        print(f"Error fetching price for {ticker}: {e}")
        return 0.0
    
def get_price_history(ticker: str, period:str = "6mo"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist