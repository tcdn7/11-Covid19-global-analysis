from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_missing_ratios_bar(
    missing_ratio: pd.Series,
    top_n: int = 20,
    title: str = "Top columns by missing value ratio",
) -> None:

    missing_top = missing_ratio.head(top_n)[::-1]

    plt.figure(figsize=(10, 6))
    missing_top.plot(kind="barh")
    plt.title(title)
    plt.xlabel("Missing ratio")
    plt.ylabel("Column")
    plt.tight_layout()
    plt.show()


def plot_metric_bar(
    df: pd.DataFrame,
    metric_col: str,
    title: str,
    xlabel: str,
    figsize: tuple[int, int] = (8, 5),
) -> None:

    if metric_col not in df.columns:
        raise KeyError(f"Column '{metric_col}' is not in the dataframe.")

    data = df.sort_values(metric_col, ascending=True)

    plt.figure(figsize=figsize)
    plt.barh(data["location"], data[metric_col])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Country")

    for i, v in enumerate(data[metric_col]):
        plt.text(
            v,
            i,
            f" {v}",
            va="center",
            fontsize=9,
        )

    plt.tight_layout()
    plt.show()


def plot_vaccination_vs_cfr(
    df: pd.DataFrame,
    vacc_col: str = "vaccination_coverage",
    cfr_col: str = "case_fatality_ratio",
    hue_col: str | None = "location",
    title: str = "Vaccination coverage vs case fatality ratio",
) -> None:

    if vacc_col not in df.columns or cfr_col not in df.columns:
        raise KeyError("Vaccination / CFR columns are missing from dataframe.")

    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=df,
        x=vacc_col,
        y=cfr_col,
        hue=hue_col,
        s=80,
    )
    plt.title(title)
    plt.xlabel("Vaccination coverage (%)")
    plt.ylabel("Case fatality ratio")
    plt.tight_layout()
    plt.show()
