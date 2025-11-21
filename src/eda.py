from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


def print_basic_info(df: pd.DataFrame) -> None:

    n_rows, n_cols = df.shape
    print(f"Number of rows: {n_rows:,}")
    print(f"Number of columns: {n_cols}")
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nData types:")
    print(df.dtypes.value_counts())


def compute_missing_ratios(df: pd.DataFrame) -> pd.Series:

    return df.isna().mean().sort_values(ascending=False)


def get_latest_per_country(
    df: pd.DataFrame,
    country_col: str = "location",
    date_col: str = "date",
    subset_cols: Iterable[str] | None = None,
) -> pd.DataFrame:

    if date_col not in df.columns or country_col not in df.columns:
        raise KeyError("Expected columns not found in dataframe.")

    df_sorted = df.sort_values([country_col, date_col])
    latest = (
        df_sorted.groupby(country_col, as_index=False).tail(1).reset_index(drop=True)
    )

    if subset_cols is not None:
        subset_cols = list(set(subset_cols) | {country_col, date_col})
        latest = latest[subset_cols]

    return latest
