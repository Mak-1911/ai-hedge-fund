import pandas as pd
from src.graph.state import AgentState
from src.risk.manager import RiskManager
from src.portfolio.manager import PortfolioManager
from src.tools.api import get_price_history

def run_backtest(ticker: str, agent_module, period: str = "6mo", cash: float = 10000.0):
    """Run a backtest for a single ticker with a given agent."""
    hist = get_price_history(ticker, period=period)
    if hist is None or hist.empty:
        raise ValueError(f"No historical data found for {ticker}")

    rm = RiskManager()
    pm = PortfolioManager()

    portfolio_history = []
    state = AgentState(ticker=ticker, cash=cash, portfolio_value=cash)

    for date, row in hist.iterrows():
        state.price = row["Close"]

        # Agent generates signal
        state = agent_module.analyze(state)

        # Risk manager adjusts
        state = rm.process(state)

        # Portfolio manager executes
        state = pm.process(state)

        portfolio_history.append({
            "date": date,
            "cash": state.cash,
            "holdings": state.holdings,
            "value": state.portfolio_value
        })

    df = pd.DataFrame(portfolio_history).set_index("date")
    return df