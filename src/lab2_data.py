"""Load the same original CSVs and chronological split for every notebook."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TRAIN_RATIO = 0.80
SEASON_LENGTH = 12


def _monthly(frame, date_column, value_column):
    dates = pd.to_datetime(frame[date_column], errors='raise')
    if dates.duplicated().any():
        raise ValueError('Duplicate timestamps in source CSV.')
    values = pd.to_numeric(frame[value_column], errors='raise').to_numpy(dtype=float)
    series = pd.Series(values, index=pd.DatetimeIndex(dates), name=value_column).sort_index()
    monthly = series.asfreq('MS')
    if len(monthly) != len(series) or monthly.isna().any() or not np.isfinite(monthly).all():
        raise ValueError('Missing monthly observations or invalid target values.')
    return monthly


def load_datasets():
    raw1 = pd.read_csv(ROOT / 'data/a10.csv')
    raw2 = pd.read_csv(ROOT / 'data/airline-passengers.csv')
    y1 = _monthly(raw1, 'date', 'value')
    y2 = _monthly(raw2, 'Month', 'Passengers')
    return raw1, raw2, y1, y2


def chronological_split(series, ratio=TRAIN_RATIO):
    if not 0 < ratio < 1:
        raise ValueError('Train ratio must be between 0 and 1.')
    cut = int(len(series) * ratio)
    if cut == 0 or cut == len(series):
        raise ValueError('Both train and test must contain observations.')
    train, test = series.iloc[:cut].copy(), series.iloc[cut:].copy()
    assert train.index[-1] < test.index[0]
    return train, test
