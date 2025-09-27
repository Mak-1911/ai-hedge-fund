# src/agents/buffett.py
from ..graph.state import AgentState
from ..tools.api import get_price_history, get_latest_price

def analyze(state: AgentState) -> AgentState:
    """Warren Buffett Agent — looks for stability and fair price."""
    try:
        ticker = state.ticker
        price = state.price or get_latest_price(ticker)
        hist = get_price_history(ticker, period="6mo")

        if hist is None or hist.empty:
            state.agent_signal = {"action": "hold", "confidence": 0.5}
            state.signals["Buffett"] = state.agent_signal
            state.reasoning["Buffett"] = f"No price history found for {ticker}, default HOLD."
            return state

        volatility = hist["Close"].pct_change().std() * 100  # % volatility

        if volatility < 2:  # very stable
            action, conf = "buy", 0.8
        elif volatility < 5:  # moderate
            action, conf = "hold", 0.6
        else:  # too volatile
            action, conf = "sell", 0.7

        state.agent_signal = {"action": action, "confidence": conf}
        state.signals["Buffett"] = state.agent_signal
        state.reasoning["Buffett"] = (
            f"Volatility = {volatility:.2f}%. Interpreted as {action.upper()} ({conf*100:.0f}%)."
        )

    except Exception as e:
        state.agent_signal = {"action": "hold", "confidence": 0.5}
        state.signals["Buffett"] = state.agent_signal
        state.reasoning["Buffett"] = f"Error during Buffett analysis: {e}"

    return state
