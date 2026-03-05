from time import sleep
import yfinance as yf
import pandas as pd

TICKERS = {"spx": "^GSPC", "gold": "GC=F"}


def fetch(start: str, end: str, retries: int = 3) -> pd.DataFrame:
    data = {}
    for name, ticker in TICKERS.items():
        for attempt in range(retries):
            raw = yf.download(
                ticker, start=start, end=end, auto_adjust=True, progress=False
            )
            if raw is not None and not raw.empty:
                break
            sleep(5 * (attempt + 1))
        else:
            raise ValueError(f"No data returned for {ticker} between {start} and {end}")
        data[name] = raw["Close"].iloc[:, 0] if raw["Close"].ndim > 1 else raw["Close"]
        sleep(2)
    return pd.DataFrame(data)
