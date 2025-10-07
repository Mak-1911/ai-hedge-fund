from ..graph.state import AgentState

class PortfolioManager:
    def process(self, state: AgentState) -> AgentState:
        # Implement portfolio management logic here
        try: 
            action = state.agent_signal.action if state.agent_signal else "hold"
            price = state.price or 0.0

            # default: no trade
            order = {"action": "hold", "size": 0}
            if action == "buy" and state.cash >= price and price > 0:
                # Only buy if we have enough cash and price is valid
                # Calculate position size (simple strategy: use 10% of available cash)
                position_size = max(1, int((state.cash * 0.1) / price))
                # Ensure we don't spend more cash than we have
                max_affordable = int(state.cash / price)
                position_size = min(position_size, max_affordable)
                
                if position_size > 0:
                    order = {"action": "buy", "size": position_size}
                    state.holdings += position_size
                    state.cash -= position_size * price
                    state.reasoning["PortfolioManager"] = (
                        f"BUY {position_size} shares at {price:.2f}. Holdings now {state.holdings}, "
                        f"cash {state.cash:.2f}."
                    )
                else:
                    state.reasoning["PortfolioManager"] = (
                        f"Wanted to BUY but couldn't afford any shares at {price:.2f}. "
                        f"Cash available: {state.cash:.2f}."
                    )
            elif action == "sell" and state.holdings > 0:
                # Sell a portion of holdings (25% or at least 1 share)
                position_size = max(1, int(state.holdings * 0.25))
                order = {"action": "sell", "size": position_size}
                state.holdings -= position_size
                state.cash += position_size * price
                state.reasoning["PortfolioManager"] = (
                    f"SELL {position_size} shares at {price:.2f}. Holdings now {state.holdings}, "
                    f"cash {state.cash:.2f}."
                )
            else:
                state.reasoning["PortfolioManager"] = (
                    f"HOLD decision, no trade executed. "
                    f"Action: {action}, Cash: {state.cash:.2f}, Holdings: {state.holdings}, Price: {price:.2f}"
                )
            state.portfolio_value = state.cash + (state.holdings * price)
            state.final_order = order
        except Exception as e:
            state.final_order = {"action": "hold", "size": 0}
            state.reasoning["PortfolioManager"] = f"Error during portfolio management: {e}"
        return state