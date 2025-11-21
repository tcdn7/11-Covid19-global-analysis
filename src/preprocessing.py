from __future__ import annotations
from typing import Union
from pathlib import Path

import pandas as pd
import numpy as np


def filter_country_level_rows(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    if "iso_code" not in df.columns:
        raise KeyError("Column 'iso_code' is missing from the dataset.")

    mask_notna = df["iso_code"].notna()
    mask_not_owid = ~df["iso_code"].astype(str).str.startswith("OWID_")

    filtered = df.loc[mask_notna & mask_not_owid].copy()
    return filtered


def clean_covid_data(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    if "date" not in df.columns:
        raise KeyError("Column 'date' is missing from the dataset.")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    sort_cols = [col for col in ["location", "date"] if col in df.columns]
    if sort_cols:
        df = df.sort_values(sort_cols).reset_index(drop=True)

    non_negative_cols = [
        "new_cases",
        "new_deaths",
        "new_cases_per_million",
        "new_deaths_per_million",
        "new_tests",
        "new_tests_per_thousand",
        "hosp_patients",
        "icu_patients",
    ]

    for col in non_negative_cols:
        if col in df.columns:
            neg_mask = df[col] < 0
            if neg_mask.any():
                df.loc[neg_mask, col] = np.nan

    if "population" in df.columns:
        df = df[df["population"].notna()].copy()

    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    sort_cols = [col for col in ["location", "date"] if col in df.columns]
    if sort_cols:
        df = df.sort_values(sort_cols).reset_index(drop=True)

    groupby_cols = ["location"]
    can_group = all(col in df.columns for col in groupby_cols)

    if can_group:
        grouped = df.groupby("location", group_keys=False)

        rolling_specs = {
            "new_cases_per_million": "new_cases_pm_7d_avg",
            "new_deaths_per_million": "new_deaths_pm_7d_avg",
            "stringency_index": "stringency_index_7d_avg",
        }

        for source_col, target_col in rolling_specs.items():
            if source_col in df.columns:
                df[target_col] = grouped[source_col].transform(
                    lambda s: s.rolling(window=7, min_periods=3).mean()
                )

    if "total_cases" in df.columns and "total_deaths" in df.columns:
        df["case_fatality_ratio"] = np.where(
            df["total_cases"] > 100,
            df["total_deaths"] / df["total_cases"],
            np.nan,
        )

    vaccination_coverage = None

    if "people_fully_vaccinated_per_hundred" in df.columns:
        vaccination_coverage = "people_fully_vaccinated_per_hundred"
    elif "people_vaccinated_per_hundred" in df.columns:
        vaccination_coverage = "people_vaccinated_per_hundred"

    if vaccination_coverage is not None:
        df["vaccination_coverage"] = df[vaccination_coverage]

    return df


def build_clean_feature_dataset(df_raw: pd.DataFrame) -> pd.DataFrame:

    df = filter_country_level_rows(df_raw)
    df = clean_covid_data(df)
    df = add_features(df)
    return df
