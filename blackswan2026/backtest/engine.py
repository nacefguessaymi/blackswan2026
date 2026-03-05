import pandas as pd
import numpy as np

from blackswan2026.backtest.analysis import (
    annualized_return,
    volatility,
    sharpe_ratio,
    max_drawdown,
    compute_corr_matrix,
    minimum_variance_weights,
)
from blackswan2026.retrieve import fetch_all


def load_data(start: str, end: str) -> pd.DataFrame:
    prices = fetch_all(start, end)
    prices = prices.ffill().dropna()
    return prices


def compute_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna()


def run(start: str, end: str, capital: float = 1000.0) -> dict:
    prices = load_data(start, end)
    returns = compute_returns(prices)
    weights = minimum_variance_weights(returns)
    portfolio_returns = (returns[weights.index] * weights).sum(axis=1)
    equity_curve = capital * (1 + portfolio_returns).cumprod()
    return {
        "weights": weights,
        "portfolio_returns": portfolio_returns,
        "volatility": volatility(portfolio_returns),
        "equity_curve": equity_curve,
        "sharpe": sharpe_ratio(
            portfolio_returns, risk_free_rate=returns["fed_funds"].mean()
        ),
        "max_drawdown": max_drawdown(portfolio_returns),
        "annualized_return": annualized_return(portfolio_returns),
        "corr_matrix": compute_corr_matrix(returns),
    }
