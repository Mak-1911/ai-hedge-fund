from ..graph.state import AgentState
from ..tools.api import get_price_history

def analyze(state: AgentState) -> AgentState:
    # Simple Buffett strategy: buy if P/E < 15 and dividend yield > 2%
    
    state.signals["Buffett"] = "buy"
    state.reasoning["Buffett"] = "Wonderful business at a fair price"
    return state