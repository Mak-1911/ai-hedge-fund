import argparse
from importlib import import_module
from InquirerPy import inquirer
from src.graph.state import AgentState
from src.tools.api import get_latest_price
from src.risk.manager import RiskManager
from src.portfolio.manager import PortfolioManager
from rich.console import Console
from rich.table import Table
from src.metrics.runner import MetricsRunner
import pandas as pd
from src.backtest.engine import run_backtest

console = Console()

AGENT_MAP = {
    "valuation": "src.agents.valuation_analyst",
    "buffett": "src.agents.warren_buffet",
    "jhunjhunwala": "src.agents.rakesh_jhunjhunwala",
}

def load_agent_module(name: str):
    if name not in AGENT_MAP:
        raise ValueError(f"Unknown agent '{name}'. choose from {list(AGENT_MAP.keys())}")
    return import_module(AGENT_MAP[name])

def choose_agent_interactively():
    agent_name = inquirer.select(
        message="Choose an agent:",
        choices=list(AGENT_MAP.keys()),
        default="valuation",
    ).execute()
    return agent_name

def summarize_performance(df):
    returns = df["value"].pct_change().dropna()
    cumulative = (df["value"].iloc[-1] / df["value"].iloc[0]) - 1
    sharpe = returns.mean() / returns.std() * (252**0.5) if not returns.empty else 0
    max_dd = (df["value"] / df["value"].cummax() - 1).min()

    print("\n=== Performance Metrics ===")
    print(f"Cumulative Return: {cumulative:.3f}")
    print(f"Sharpe Ratio: {sharpe:.3f}")
    print(f"Max Drawdown: {max_dd:.3f}")


def run_single(ticker: str, agent_name: str, cash_portfolio: float = 10000.0, cash: float = 10000.0):
    price = get_latest_price(ticker)
    state = AgentState(ticker=ticker, price=price, cash=cash, holdings=0)
    state.portfolio_value = cash_portfolio
    rm = RiskManager()
    pm = PortfolioManager()
    mr = MetricsRunner()
    mod = load_agent_module(agent_name)
    state = mod.analyze(state)
    state = rm.process(state)
    state = pm.process(state)
    state = mr.process(state)

     # Print decision flow
    console.print("\n[bold cyan]=== Decision Flow ===[/bold cyan]")
    for actor, reason in state.reasoning.items():
        console.print(f"[green][{actor}][/green] {reason}")


     # Final summary table
    table = Table(title=f"{agent_name.title()} Agent Result")

    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    table.add_row("Ticker", state.ticker)
    table.add_row("Latest Price", f"{state.price:.2f}")
    table.add_row("Signal", str(state.agent_signal))
    table.add_row("Risk", str(state.risk))
    table.add_row("Final Order", str(state.final_order))
    table.add_row("Cash", f"{state.cash:.2f}")
    table.add_row("Holdings", str(state.holdings))
    table.add_row("Portfolio Value", f"{state.portfolio_value:.2f}")
    if state.metrics:
        table.add_row("Cumulative Return", f"{state.metrics['cumulative_return']:.2%}")
        table.add_row("Sharpe Ratio", f"{state.metrics['sharpe_ratio']:.2f}")
        table.add_row("Max Drawdown", f"{state.metrics['max_drawdown']:.2%}")

    console.print(table)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--agent", help="choose agent (if not passed, interactive menu appears)")
    parser.add_argument("--backtest", action="store_true")
    parser.add_argument("--period", default="1y")
    parser.add_argument("--cash", type=float, default=10000.0)
    args = parser.parse_args()

    agent_name = args.agent or choose_agent_interactively()

    if args.backtest:
        agent_module = load_agent_module(agent_name)
        print(f"Running backtest for {args.ticker} with {agent_name} agent...")
        results = run_backtest(args.ticker, agent_module, period=args.period, cash=args.cash)

        print("\n=== Backtest Results ===")
        print(results.tail())

        summarize_performance(results)
    else:
        run_single(args.ticker, agent_name, cash_portfolio=args.cash)

if __name__ == "__main__":
    main()
