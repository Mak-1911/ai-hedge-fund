import yfinance as yf
from src.agents.warren_buffet import analyze
from src.graph.state import AgentState

# Create a test state
state = AgentState(ticker="AAPL", price=250.0, cash=10000.0, holdings=0)

# Run the Buffett agent analysis
state = analyze(state)

# Print the results
print("Agent Signal:", state.agent_signal)
print("Signals:", state.signals)
print("Reasoning:", state.reasoning)
print("Risk:", state.risk)