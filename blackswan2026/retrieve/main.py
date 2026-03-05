import pandas as pd

from blackswan2026.retrieve.sources import fred_fetch, yf_fetch


def fetch_all(start: str, end: str) -> pd.DataFrame:
    fred_data = fred_fetch(start, end)
    yf_data = yf_fetch(start, end)
    return pd.concat([fred_data, yf_data], axis=1)
