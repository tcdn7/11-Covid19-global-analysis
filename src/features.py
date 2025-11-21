from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd


def add_group_rolling_mean(
    df: pd.DataFrame,
    group_col: str,
    value_cols: Sequence[str],
    window: int = 7,
    min_periods: int = 3,
    suffix: str = "7d_avg",
) -> pd.DataFrame:

    df = df.copy()
    df = df.sort_values([group_col, "date"])

    grouped = df.groupby(group_col, group_keys=False)

    for col in value_cols:
        if col not in df.columns:
            continue

        new_col = f"{col}_{suffix}"
        df[new_col] = grouped[col].transform(
            lambda s: s.rolling(window=window, min_periods=min_periods).mean()
        )

    return df


def add_case_fatality_ratio(
    df: pd.DataFrame,
    total_cases_col: str = "total_cases",
    total_deaths_col: str = "total_deaths",
    min_cases: int = 100,
    new_col: str = "case_fatality_ratio",
) -> pd.DataFrame:

    df = df.copy()

    if total_cases_col not in df.columns or total_deaths_col not in df.columns:
        raise KeyError("total_cases / total_deaths columns are missing from dataframe.")

    mask = df[total_cases_col] > min_cases
    df[new_col] = np.where(
        mask,
        df[total_deaths_col] / df[total_cases_col],
        np.nan,
    )
    return df
