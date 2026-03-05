from scipy.optimize import minimize
import pandas as pd
import numpy as np

BOUNDS = {"spx": (-1, 0), "wti": (0, 1), "gold": (0, 1)}


def minimum_variance_weights(returns: pd.DataFrame) -> pd.Series:
    returns = pd.DataFrame(returns[list(BOUNDS.keys())])
    cov = returns.cov()

    def portfolio_variance(w):
        return w.T @ cov.values @ w

    constraints = {"type": "eq", "fun": lambda w: w.sum() - 1}
    bounds = [BOUNDS[col] for col in returns.columns]
    w0 = np.array([b[0] + (b[1] - b[0]) / 2 for b in bounds])

    result = minimize(portfolio_variance, w0, bounds=bounds, constraints=constraints)
    return pd.Series(result.x, index=returns.columns)
