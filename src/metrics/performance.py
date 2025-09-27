import numpy as np
import pandas as pd

def compute_returns(price_series: pd.Series) -> pd.Series:
    """Compute daily returns from price series."""
    returns = price_series.pct_change().fillna(0)
    return returns

def cumulative_return(price_series: pd.Series) -> float:
    """Total return over the period"""
    returns = compute_returns(price_series)
    return (1+returns).prod() - 1

def sharpe_ratio(price_series: pd.Series, risk_free_rate: float = 0.0) -> float:
    """Annualized Sharpe Ratio"""
    returns = compute_returns(price_series)
    excess = returns - risk_free_rate/252
    if (excess.std() == 0).all():
        return 0
    return np.sqrt(252) * excess.mean() / excess.std()


def max_drawdown(price_series:pd.Series) -> float:
    """Maximum Drawdown ( Worst peak-to-trough decline)"""
    cumulative = price_series / price_series.iloc[0]
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    return drawdown.min()