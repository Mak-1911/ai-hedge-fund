from ..graph.state import AgentState

def analyze(state: AgentState) -> AgentState:
    state.signals["Jhunjhunwala"] = "buy"
    state.reasoning["Jhunjhunwala"] = "The Big Bull sees opportunity"
    return state