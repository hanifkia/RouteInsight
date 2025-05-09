import os
import sys

import pandas as pd
import streamlit as st

sys.path.append("..")

from config import DATA_PATH, DEFAULT_FILE_NAME


def load_data() -> pd.DataFrame:
    """Load forecast data from a CSV file specified by an environment variable."""
    file_name = os.getenv("FORECAST_FILE_NAME", DEFAULT_FILE_NAME)
    file_path = DATA_PATH.format(file_name)

    try:
        df = pd.read_csv(file_path, parse_dates=["timestamp"]).drop("region_id", axis=1)
        return df
    except FileNotFoundError:
        st.error(
            f"File {file_path} not found. Please check the FORECAST_FILE_NAME environment variable."
        )
        return pd.DataFrame()
