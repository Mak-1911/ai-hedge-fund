from ..graph.state import AgentState
from ..tools.api import get_price_history

class RiskManager:
    def process(self, state: AgentState) -> AgentState:
        try:
            hist = get_price_history(state.ticker, period="3mo")

            if hist is None or hist.empty:
                state.risk = {"volatility": None}
                state.reasoning["RiskManager"] = (
                    f"No historical data for {state.ticker}, skipping risk analysis."
                )
                return state

            volatility = hist["Close"].pct_change().std() * 100  # %
            state.risk = {"volatility": volatility}

            # reasoning
            if volatility > 5:
                state.reasoning["RiskManager"] = (
                    f"Volatility = {volatility:.2f}%. High risk, reduce confidence."
                )
                # adjust confidence down slightly
                if state.agent_signal:
                    state.agent_signal["confidence"] = max(
                        0.1, state.agent_signal["confidence"] - 0.2
                    )
            else:
                state.reasoning["RiskManager"] = (
                    f"Volatility = {volatility:.2f}%. Stable, confidence intact."
                )

        except Exception as e:
            state.risk = {"volatility": None}
            state.reasoning["RiskManager"] = f"Error during risk analysis: {e}"

        return state
