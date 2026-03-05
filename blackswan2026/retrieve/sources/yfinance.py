import yfinance as yf
import pandas as pd

DEFAULT_TICKERS = {"spx": "^GSPC", "gold": "GC=F"}


def fetch(
    start: str, end: str, tickers: dict[str, str] = DEFAULT_TICKERS
) -> pd.DataFrame:
    """
    Fetch historical price data from Yahoo Finance.

    Args:
        start: Start date in YYYY-MM-DD format.
        end: End date in YYYY-MM-DD format.
        tickers: Mapping of name to Yahoo Finance ticker symbol.
                 Defaults to SPX and gold futures.

    Returns:
        DataFrame with dates as index and ticker names as columns.

    Raises:
        ValueError: If no data is returned for the given date range.
    """
    t = yf.Tickers(" ".join(tickers.values()))
    raw = t.download(start=start, end=end, auto_adjust=True, progress=False)

    if raw is None or raw.empty:
        raise ValueError(f"No data returned between {start} and {end}")

    data = {}
    for name, ticker in tickers.items():
        series = raw["Close"][ticker]
        data[name] = series

    return pd.DataFrame(data)
