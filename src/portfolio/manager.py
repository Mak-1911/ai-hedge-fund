from ..graph.state import AgentState

class PortfolioManager:
    def process(self, state: AgentState) -> AgentState:
        # Implement portfolio management logic here
        try: 
            action = state.agent_signal.action if state.agent_signal else "hold"
            price = state.price or 0.0
            print(f"DEBUG: Attempting BUY. Cash={state.cash}, Price={price}")

            # default: no trade
            order = {"action": "hold", "size": 0}
            if action == "buy" :
                print(f"DEBUG: Attempting BUY. Cash={state.cash}, Price={price}")
                order = {"action":"buy", "size":1}
                state.holdings += 1
                state.cash -= price
                state.reasoning["PortfolioManager"]=(
                    f"BUY 1 share at {price:.2f}. Holdings now {state.holdings}, "
                    f"cash {state.cash:.2f}."
                )
            elif action == "sell" and state.holdings > 0:
                order = {"action":"sell", "size":1}
                state.holdings -= 1
                state.cash += price
                state.reasoning["PortfolioManager"] = (
                    f"SELL 1 share at {price:.2f}. Holdings now {state.holdings}, "
                    f"cash {state.cash:.2f}."
                )
            else:
                state.reasoning["PortfolioManager"] = (
                    f"HOLD decision, no trade executed."
                )
            state.portfolio_value = state.cash + (state.holdings * price)
            state.final_order = order
        except Exception as e:
            state.final_order = {"action": "hold", "size": 0}
            state.reasoning["PortfolioManager"] = f"Error during portfolio management: {e}"
        return state