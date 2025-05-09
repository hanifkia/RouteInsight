import numpy as np
import streamlit as st
from data.loader import load_data
from data.preprocessor import filter_data, preprocess_data
from utils.export import create_export_link, create_weekly_report
from visualization.charts import (
    create_overall_route_counts_chart,
    create_weekly_forecast_chart,
)
from visualization.tables import (
    create_route_counts_over_time_table,
    create_route_counts_per_region_table,
)


def create_region_selector(data) -> list[str]:
    """Create a region selector in the sidebar with an 'All' option."""
    st.sidebar.header("Filters")
    st.sidebar.text("Select Region(s)")

    select_all = st.sidebar.checkbox("All", value=True)
    selected_regions = []

    if select_all:
        selected_regions = list(data["region_name"].unique())
        for region in data["region_name"].unique():
            st.sidebar.checkbox(region, value=False)
    else:
        for region in data["region_name"].unique():
            if st.sidebar.checkbox(region, value=False):
                selected_regions.append(region)

    return selected_regions if selected_regions else []


def create_time_range_selector(weeks_dict) -> tuple[str, str]:
    """Create a time range selector in the sidebar."""
    time_ranges = list(weeks_dict.keys())
    time_ranges = list(np.roll(time_ranges, 1))  # Rotate to prioritize 'All'
    selected_range = st.sidebar.radio("Select Time Range", time_ranges)
    return weeks_dict[selected_range]


def main():
    """Main function to run the Streamlit dashboard."""
    st.set_page_config(layout="wide")

    # Load and preprocess data
    df = load_data()
    if df.empty:
        return

    data, future, weeks_dict = preprocess_data(df)

    # Sidebar filters
    selected_regions = create_region_selector(data)
    date_range = create_time_range_selector(weeks_dict)

    # Filter data
    data_filtered = filter_data(data, selected_regions, date_range)

    # First Row: Two Columns
    col1, col2 = st.columns(2)

    with col1:
        # Overall Route Counts Chart
        fig1, err = create_overall_route_counts_chart(data_filtered)
        st.markdown("##### Overall Route Counts per Selected Region(s)")
        st.text(f"Error: {err}%")
        st.plotly_chart(fig1, use_container_width=True, key="values_bars")

        # Route Counts Over Time Table
        route_counts_table = create_route_counts_over_time_table(data_filtered)
        st.markdown("##### Route Counts by Selected Region(s) Over Time")
        st.dataframe(route_counts_table, use_container_width=True, height=250)

    with col2:
        # Weekly Forecast Chart
        st.markdown("##### Next Week Route Traffic Insights")
        fig2 = create_weekly_forecast_chart(future, selected_regions)

        # Export Weekly Report
        weekly_report = create_weekly_report(future, selected_regions)
        export_link = create_export_link(weekly_report)
        if export_link:
            st.markdown(export_link, unsafe_allow_html=True)
        else:
            st.warning("No data available to export.")

        st.plotly_chart(fig2, use_container_width=True, key="forecast_bars")

        # Route Counts Per Region Table
        region_counts_table = create_route_counts_per_region_table(data)
        st.markdown("##### Route Counts per Region")
        st.dataframe(region_counts_table, use_container_width=True, height=250)


if __name__ == "__main__":
    main()
