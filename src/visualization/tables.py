import pandas as pd


def create_route_counts_over_time_table(data_filtered: pd.DataFrame) -> pd.DataFrame:
    """Create a table for route counts over time by region."""
    tmp = (
        data_filtered.drop(["week_number", "month_name"], axis=1)
        .sort_values(by=["region_name", "timestamp"])
        .groupby(["region_name", "timestamp"])
        .sum()
        .reset_index()
    )
    tmp["timestamp"] = tmp["timestamp"].apply(lambda x: x.date())
    return tmp


def create_route_counts_per_region_table(data: pd.DataFrame) -> pd.DataFrame:
    """Create a table for route counts per region."""
    return (
        data.drop(["month_name", "day_of_week", "week_number"], axis=1)
        .set_index(["region_name", "timestamp"])
        .groupby("region_name")
        .sum()
        .reset_index()
        .rename(
            columns={
                "region_name": "Region",
                "value": "Actual",
                "lower": "Lower",
                "forecast": "Forecast",
                "upper": "Upper",
            }
        )
    )
