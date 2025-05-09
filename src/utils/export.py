import base64
from datetime import datetime

import pandas as pd
import streamlit as st


def create_export_link(weekly_report: pd.DataFrame) -> str:
    """Create a downloadable CSV link for the weekly report."""
    if weekly_report is not None and not weekly_report.empty:
        csv = weekly_report.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        timestamp = str(datetime.now())[:-7].replace(":", "-").replace(" ", "-")
        return f'<a href="data:file/csv;base64,{b64}" download="forecast_data_{timestamp}.csv">Export to CSV</a>'
    return None


def create_weekly_report(
    future: pd.DataFrame, selected_regions: list[str]
) -> pd.DataFrame:
    """Prepare the weekly report data for export."""
    return (
        future[future["region_name"].isin(selected_regions)]
        .drop("value", axis=1)
        .rename(
            columns={
                "region_name": "Region",
                "timestamp": "Date",
                "lower": "Lower",
                "forecast": "Forecast",
                "upper": "Upper",
            }
        )
        .sort_values(by=["Region", "Date"])
        .reset_index(drop=True)
    )
