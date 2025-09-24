from ..graph.state import AgentState
from ..tools.api import get_price_history
from ..graph import state

def analyze(state: AgentState) -> AgentState:
    try:
        hist = get_price_history(state.ticker, period="3mo")

        if hist.empty or len(hist) < 30:
            state.signals["Valuation"] = "hold"
            state.reasoning["Valuation"] = "Not enough historical data"
            return state

        
        ma30 = hist["Close"].rolling(window=30).mean().iloc[-1] # Compute 30-day moving average

        # Compare current price with MA
        if state.price < 0.9 * ma30:      
            signal = "buy"
            reason = f"Undervalued: price {state.price:.2f} < 90% of 30d avg {ma30:.2f}"
        elif state.price > 1.1 * ma30:
            signal = "sell"
            reason = f"Overvalued: price {state.price:.2f} > 110% of 30d avg {ma30:.2f}"
        else:
            signal = "hold"
            reason = f"Fairly valued: price {state.price:.2f} ~ 30d avg {ma30:.2f}"

        # Save to state
        state.signals["Valuation"] = signal
        state.reasoning["Valuation"] = reason
    except Exception as e:
        state.signals["Valuation"] = "hold"
        state.reasoning["Valuation"] = f"Error during valuation: {e}"

    return state