"""Configuration constants for the forecast dashboard."""

# File paths
DEFAULT_FILE_NAME = "results_fi_fu"
DATA_PATH = "./report/{}.csv"

# Plotting constants
YAXIS_BUFFER = 0.1  # Buffer for y-axis range (10%)
CHART_HEIGHT = 350
COLORS = {
    "Actual": "blue",
    "Lower": "#ADD8E6",
    "Forecast": "green",
    "Upper": "pink",
}
LEGEND_LAYOUT = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
