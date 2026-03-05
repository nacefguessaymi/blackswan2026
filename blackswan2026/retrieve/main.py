import os
import pandas as pd

from blackswan2026.retrieve.sources import (
    fred_fetch,
    yf_fetch,
    DEFAULT_SERIES,
    DEFAULT_TICKERS,
)

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


def _cache_path(source: str, start: str, end: str, keys: list[str]) -> str:
    key = f"{source}_{start}_{end}_{'_'.join(keys)}.parquet".replace("-", "")
    return os.path.join(CACHE_DIR, key)


def _load_cache(path: str) -> pd.DataFrame:
    if os.path.exists(path):
        return pd.read_parquet(path)
    else:
        raise ValueError(f"Path for cache {path} does not exist")


def _save_cache(df: pd.DataFrame, path: str) -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    df.to_parquet(path)


def fetch_all(start: str, end: str) -> pd.DataFrame:
    fred_data = fred_fetch(start, end)
    yf_data = yf_fetch(start, end)
    return pd.concat([fred_data, yf_data], axis=1)
