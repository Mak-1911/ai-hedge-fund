import yfinance as yf
from . import performance
from src.graph.state import AgentState

class MetricsRunner:
    def process(self, state:AgentState, period:str="6mo") -> AgentState:
        """Fetching Price History and Computing Performance Metrics"""
        try:
            data = yf.download(state.ticker, period=period, progress=False)
            prices = data["Close"]

            state.metrics = {
                "cumulative_return": performance.cumulative_return(prices),
                "sharpe_ratio": performance.sharpe_ratio(prices),
                "max_drawdown": performance.max_drawdown(prices)
            }
            state.reasoning["Metrics"] = "Computed performance metrics"
        except Exception as e:
            state.metrics = {}
            state.reasoning["Metrics"] = f"Error computing metrics: {e}"
        
        return state