from ..graph.state import AgentState
from ..tools.api import get_price_history

def analyze(state: AgentState) -> AgentState:
    try:
        hist = get_price_history(state.ticker, period="6mo")
        # if len(hist) < 30:
        #     state.signals["Jhunjhunwala"] = "HOLD"
        #     state.reasoning["Jhunjhunwala"] = "Insufficient Data for Momentum Analysis"
        #     return state
        
        ma30 = hist["Close"].rolling(window=30).mean().iloc[-1] # Compute 30-day moving average
        if state.price > ma30:
            signal = "BUY"
            reasoning = f"Price above 30-day MA ({ma30:.2f})"
        elif state.price < ma30:
            signal = "SELL"
            reasoning = f"Price below 30-day MA ({ma30:.2f})"
        else:
            signal = "HOLD"
            reasoning = "Price at 30-day MA"

        state.signals["Jhunjhunwala"] = signal
        state.reasoning["Jhunjhunwala"] = reasoning
    
    except Exception as e:
        state.signals["Jhunjhunwala"] = "HOLD"
        state.reasoning["Jhunjhunwala"] = f"Error in analysis: {str(e)}"

    return state