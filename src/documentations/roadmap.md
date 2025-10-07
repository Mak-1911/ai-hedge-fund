🚀 Roadmap
✅ Implemented So Far

CLI runner (main.py)

Interactive agent selection with arrow keys (InquirerPy).

Supports --ticker, --agent, --backtest, --cash.

AgentState (state.py)

Pydantic model for data flow between agents.

Tracks ticker, price, holdings, cash, portfolio_value, reasoning, signals, risk, final_order, metrics.

Agents (valuation, buffett, jhunjhunwala, etc.)

Each agent implements analyze(state) → AgentState.

Produces action (buy/sell/hold) + confidence.

---


Adjusts confidence/risk reasoning.

Portfolio Manager
Executes simulated trades based on agent signal.

Updates holdings, cash, portfolio_value.

Metrics Module

Computes cumulative return, Sharpe ratio, max drawdown.

Integrated into pipeline.

Summary Table Output
Shows ticker, signal, risk, portfolio, metrics.

🔜 Next Steps

Backtesting Engine

Run strategy over historical data.


Store trades + equity curve.


Multi-Agent Orchestration

Run multiple agents in sequence (Valuation → Risk → Portfolio).

Or ensemble agents with weighted voting.
Persistence Layer

Allows later analysis & dashboards.

Web Dashboard (optional)

Streamlit or FastAPI-based UI.

Upload strategies, view metrics & charts.

AI-Inspired Extensions

Natural language interface for “Explain this trade.”

LangGraph-like orchestration between agents.

Reinforcement learning agent for trade optimization.