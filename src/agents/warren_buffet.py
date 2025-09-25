from ..graph.state import AgentState
from ..tools.api import get_price_history

def analyze(state: AgentState) -> AgentState:
    # Simple Buffett strategy: buy if P/E < 15 and dividend yield > 2%
    try:
        hist = get_price_history(state.ticker, period="6mo")
        
        if hist.empty or len(hist) < 30:
            state.signals["Buffett"] = "hold"
            state.reasoning["Buffett"] = "Not enough historical data for volatility analysis"
            return state
        
        hist["Return"] = hist["Close"].pct_change()
        volatility = hist["Return"].std() * 100
        if volatility < 2:
            signal = "BUY"
            reasoning = f"Low volatility ({volatility:.2f}%), Buffett likes stable businesses"
        elif volatility > 4:
            signal = "SELL"
            reasoning = f"High volatility ({volatility:.2f}%), too risky for Buffett"
        else:
            signal = "HOLD"
            reasoning = f"Moderate volatility ({volatility:.2f}%), fairly stable"

        state.signals["Buffet"] = signal
        state.reasoning["Buffet"] = reasoning

    except Exception as e:
        state.signals["Buffet"] = "HOLD"
        state.reasoning["Buffet"] = f"Error During Buffet Analysis: {e}"
    
    return state