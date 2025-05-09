import sys

import numpy as np
import pandas as pd
import plotly.graph_objects as go

sys.path.append("..")

from config import CHART_HEIGHT, COLORS, LEGEND_LAYOUT, YAXIS_BUFFER


def create_overall_route_counts_chart(
    data_filtered: pd.DataFrame,
) -> tuple[go.Figure, float]:
    """Create a bar chart for overall route counts."""
    # Prepare data for the chart
    tmp = (
        data_filtered.drop(["month_name", "day_of_week", "week_number"], axis=1)
        .rename(
            columns={
                "region_name": "Region",
                "value": "Actual",
                "lower": "Lower",
                "forecast": "Forecast",
                "upper": "Upper",
            }
        )
        .set_index(["Region", "timestamp"])
        .sum()
        .reset_index()
        .rename(columns={0: "Route Counts", "index": "Values"})
    )

    # Calculate error percentage
    err_dict = tmp.set_index("Values").to_dict()["Route Counts"]
    err = np.round(
        (np.abs(err_dict["Actual"] - err_dict["Forecast"]) / err_dict["Actual"]) * 100,
        2,
    )

    # Create the bar chart
    fig = go.Figure()

    for value in tmp["Values"]:
        fig.add_trace(
            go.Bar(
                x=tmp[tmp["Values"] == value]["Values"],
                y=tmp[tmp["Values"] == value]["Route Counts"],
                name=value,
                marker_color=COLORS.get(value, "gray"),
                text=tmp[tmp["Values"] == value]["Route Counts"],
                textposition="outside",
            )
        )

    # Update layout
    fig.update_layout(
        barmode="group",
        yaxis_title="Route Counts",
        xaxis_title="Values",
        height=CHART_HEIGHT,
        yaxis=dict(
            range=[
                tmp["Route Counts"].min() - YAXIS_BUFFER * tmp["Route Counts"].min(),
                tmp["Route Counts"].max() + YAXIS_BUFFER * tmp["Route Counts"].max(),
            ]
        ),
        title="Values",
        legend=LEGEND_LAYOUT,
    )
    fig.update_traces(texttemplate="%{text}", textposition="outside")

    return fig, err


def create_weekly_forecast_chart(
    future: pd.DataFrame, selected_regions: list[str]
) -> go.Figure:
    """Create a weekly forecast chart with bars and lines."""
    tmp = future[future["region_name"].isin(selected_regions)]
    tmp = tmp.groupby("timestamp")[["lower", "forecast", "upper"]].sum().reset_index()

    # Create the figure
    fig = go.Figure()

    # Add bar trace for forecast
    fig.add_trace(
        go.Bar(
            x=tmp["timestamp"],
            y=tmp["forecast"],
            name="Forecast",
            marker_color="green",
            text=tmp["forecast"],
            textposition="auto",
        )
    )

    # Add line traces for upper and lower bounds
    fig.add_trace(
        go.Scatter(
            x=tmp["timestamp"],
            y=tmp["upper"],
            mode="lines+markers",
            name="Upper",
            line=dict(color="red", dash="dash"),
            marker=dict(size=8),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=tmp["timestamp"],
            y=tmp["lower"],
            mode="lines+markers",
            name="Lower",
            line=dict(color="blue", dash="dash"),
            marker=dict(size=8),
        )
    )

    # Update layout
    fig.update_layout(
        yaxis_title="Route Counts",
        height=CHART_HEIGHT,
        yaxis=dict(
            range=[
                tmp["lower"].min() - YAXIS_BUFFER * tmp["lower"].min(),
                tmp["upper"].max() + YAXIS_BUFFER * tmp["upper"].max(),
            ]
        ),
        legend=LEGEND_LAYOUT,
    )

    return fig
