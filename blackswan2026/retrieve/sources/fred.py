import os
from time import sleep
import requests
import pandas as pd

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
SERIES = {"wti": "DCOILWTICO", "fed_funds": "FEDFUNDS"}
API_KEY = os.environ["FRED_API_KEY"]


def fetch(start: str, end: str) -> pd.DataFrame:
    data = {}
    for name, sid in SERIES.items():
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
        series = pd.Series(
            {
                obs["date"]: float(obs["value"])
                for obs in observations
                if obs["value"] != "."
            }
        )
        series.index = pd.to_datetime(series.index)
        data[name] = series
        sleep(2)
    return pd.DataFrame(data)
