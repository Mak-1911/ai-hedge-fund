
from ..graph.state import AgentState
from ..tools.api import get_price_history, get_latest_price

def analyze(state: AgentState) -> AgentState:
    """DCF-lite Valuation Agent"""
    try:
        ticker = state.ticker
        price = state.price or get_latest_price(ticker)
        hist = get_price_history(ticker, period="6mo")

        if hist is None or hist.empty:
            state.agent_signal = {"action": "hold", "confidence": 0.5}
            state.signals["Valuation"] = state.agent_signal
            state.reasoning["Valuation"] = f"No price history found for {ticker}, default HOLD."
            return state

        avg_price = hist["Close"].mean()
        undervalued = price < 0.9 * avg_price
        overvalued = price > 1.1 * avg_price

        print(f"DEBUG: price={price}, avg_price={avg_price}, hist_empty={hist.empty}")

        if undervalued:
            action, conf = "buy", 0.7
        elif overvalued:
            action, conf = "sell", 0.7
        else:
            action, conf = "hold", 0.6

        state.agent_signal = {"action": action, "confidence": conf}

        # Save to state (multi-agent + explanation)
        state.signals["Valuation"] = state.agent_signal
        state.reasoning["Valuation"] = (
            f"Valuation analysis: Current price {price:.2f} vs 6mo avg {avg_price:.2f} → {action.upper()} ({conf*100:.0f}%)"
        )

    except Exception as e:
        state.agent_signal = {"action": "hold", "confidence": 0.5}
        state.signals["Valuation"] = state.agent_signal
        state.reasoning["Valuation"] = f"Error during valuation: {e}"

    return state
