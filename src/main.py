import argparse
from src.graph.state import AgentState
from src.agents import warren_buffet, rakesh_jhunjhunwala, valuation_analyst
from src.tools.api import get_latest_price
from src.backtest.backtester import Backtester

def run_agents(ticker: str):
    price = get_latest_price(ticker)
    state = AgentState(ticker=ticker, price=price)

    #Run Each Agent
    for agent in [warren_buffet, rakesh_jhunjhunwala, valuation_analyst]:
        state=agent.analyze(state)
    
    # Print results
    print(f"\nResults for {ticker} (Price: ${price}):")
    for agent, signal in state.signals.items():
        reason = state.reasoning[agent]
        print(f" - {agent}: {signal.upper()} ({reason})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Hedge Fund (Lite)")
    parser.add_argument("--ticker", type=str, required=True, help="Stock ticker")
    parser.add_argument("--backtest", action="store_true", help="Run backtest")  # <-- Add this line
    args = parser.parse_args()
    if args.backtest:
        bt = Backtester(ticker=args.ticker)
        df, summary = bt.run()
        print(df.tail())
        print("\nBacktest Summary:")
        for k, v in summary.items():
            print(f" - {k}: {v}")
    run_agents(args.ticker)