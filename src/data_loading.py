from pathlib import Path
from typing import Union

import pandas as pd

from .config import COVID_RAW_PATH


def load_covid_data(path: Union[str, Path] = COVID_RAW_PATH) -> pd.DataFrame:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found at: {path}")

    df = pd.read_csv(path)
    return df
