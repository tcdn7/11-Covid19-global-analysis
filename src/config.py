from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

COVID_RAW_PATH = RAW_DATA_DIR / "owid-covid-data.csv"
COVID_CLEAN_FEATURES_PATH = PROCESSED_DATA_DIR / "covid19_clean_features.csv"
