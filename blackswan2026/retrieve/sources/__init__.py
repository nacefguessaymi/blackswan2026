from .fred import fetch as fred_fetch
from .yfinance import fetch as yf_fetch
from .fred import DEFAULT_SERIES
from .yfinance import DEFAULT_TICKERS

__all__ = ["fred_fetch", "yf_fetch", "DEFAULT_SERIES", "DEFAULT_TICKERS"]
