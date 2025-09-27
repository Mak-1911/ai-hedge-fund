# src/agents/jhunjhunwala.py
from ..graph.state import AgentState
from ..tools.api import get_price_history, get_latest_price

def analyze(state: AgentState) -> AgentState:
    """Rakesh Jhunjhunwala Agent — momentum & growth bias."""
    try:
        ticker = state.ticker
        price = state.price or get_latest_price(ticker)
        hist = get_price_history(ticker, period="3mo")

        if hist is None or hist.empty:
            state.agent_signal = {"action": "hold", "confidence": 0.5}
            state.signals["Jhunjhunwala"] = state.agent_signal
            state.reasoning["Jhunjhunwala"] = f"No price history found for {ticker}, default HOLD."
            return state

        ma30 = hist["Close"].rolling(window=30).mean().iloc[-1]

        if price > ma30:
            action, conf = "buy", 0.75
        elif price < ma30 * 0.95:
            action, conf = "sell", 0.65
        else:
            action, conf = "hold", 0.6

        state.agent_signal = {"action": action, "confidence": conf}
        state.signals["Jhunjhunwala"] = state.agent_signal
        state.reasoning["Jhunjhunwala"] = (
            f"Price {price:.2f} vs 30d MA {ma30:.2f} → {action.upper()} ({conf*100:.0f}%)."
        )

    except Exception as e:
        state.agent_signal = {"action": "hold", "confidence": 0.5}
        state.signals["Jhunjhunwala"] = state.agent_signal
        state.reasoning["Jhunjhunwala"] = f"Error during Jhunjhunwala analysis: {e}"

    return state
