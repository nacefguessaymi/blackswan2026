import numpy as np
import pandas as pd


def annualized_return(returns: pd.Series, periods: int = 252) -> float:
    return (1 + returns.mean()) ** periods - 1


def volatility(returns: pd.Series, periods: int = 252) -> float:
    return returns.std() * np.sqrt(periods)


def sharpe_ratio(
    returns: pd.Series, risk_free_rate: float = 0.0, periods: int = 252
) -> float:
    excess_returns = returns - risk_free_rate / periods
    return (excess_returns.mean() / excess_returns.std()) * np.sqrt(periods)


def max_drawdown(returns: pd.Series) -> float:
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()


def compute_corr_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    return returns.corr()
