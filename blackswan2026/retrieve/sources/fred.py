import os
from time import sleep
import requests
import pandas as pd

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
DEFAULT_SERIES = {"wti": "DCOILWTICO", "fed_funds": "FEDFUNDS"}
API_KEY = os.environ["FRED_API_KEY"]


def fetch(
    start: str, end: str, series: dict[str, str] = DEFAULT_SERIES
) -> pd.DataFrame:
    """
    Fetch economic time series data from the FRED API.

    Args:
        start: Start date in YYYY-MM-DD format.
        end: End date in YYYY-MM-DD format.
        series: Mapping of name to FRED series ID.
                Defaults to WTI crude oil and federal funds rate.

    Returns:
        DataFrame with dates as index and series names as columns.

    Raises:
        KeyError: If FRED_API_KEY environment variable is not set.
        requests.HTTPError: If the FRED API returns an error response.
    """
    data = {}
    for name, sid in series.items():
        response = requests.get(
            BASE_URL,
            params={
                "series_id": sid,
                "observation_start": start,
                "observation_end": end,
                "api_key": API_KEY,
                "file_type": "json",
            },
        )
        observations = response.json()["observations"]
        s = pd.Series(
            {
                obs["date"]: float(obs["value"])
                for obs in observations
                if obs["value"] != "."
            },
            name=name,
        )
        s.index = pd.to_datetime(s.index)
        data[name] = s
        sleep(2)
    return pd.DataFrame(data)
