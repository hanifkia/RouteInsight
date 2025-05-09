from typing import Dict, Tuple

import numpy as np
import pandas as pd


def preprocess_data(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Tuple[str, str]]]:
    """Preprocess the data: clean, add date features, and create time range dictionary."""
    # Clean data and split into historical and future datasets
    data = df.dropna().reset_index(drop=True)
    future = df[df["value"].isnull()].copy()

    # Add date-related columns
    data["month_name"] = data["timestamp"].dt.strftime("%B")
    data["day_of_week"] = data["timestamp"].dt.strftime("%A")
    data["week_number"] = data["timestamp"].dt.isocalendar().week

    # Create time range dictionary for filtering
    weeks_dict = {}
    start_date = None
    end_date = None
    for week_num in data["week_number"].unique()[-2:]:
        week_data = data[data["week_number"] == week_num]
        date_range = (
            str(week_data["timestamp"].min().date()),
            str(week_data["timestamp"].max().date()),
        )
        if not start_date:
            start_date = date_range[0]
        weeks_dict[f"{date_range[0]} - {date_range[1]}"] = date_range
    if not end_date:
        end_date = date_range[1]
    weeks_dict["All"] = (start_date, end_date)

    return data, future, weeks_dict


def filter_data(
    data: pd.DataFrame, selected_regions: list[str], date_range: Tuple[str, str]
) -> pd.DataFrame:
    """Filter data based on selected regions and date range."""
    filtered = data[data["region_name"].isin(selected_regions)].copy()
    return filtered[filtered["timestamp"].between(*date_range)]
