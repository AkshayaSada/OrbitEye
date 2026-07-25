try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

import pandas as pd
import numpy as np
from datetime import datetime

def generate_dashboard_metrics(history):
    """
    Computes summary KPIs:
    - total_images: int
    - avg_processing_time: float (seconds)
    - avg_affected_area: float (%)
    - most_common_disaster: str
    - today_count: int
    """
    if not history:
        return {
            "total_images": 0,
            "avg_processing_time": 0.0,
            "avg_affected_area": 0.0,
            "most_common_disaster": "N/A",
            "today_count": 0
        }

    df = pd.DataFrame(history)
    total_images = len(df)
    avg_processing_time = round(df["processing_time"].mean(), 3)
    avg_affected_area = round(df["affected_area"].mean(), 1)
    
    counts = df["disaster_type"].value_counts()
    most_common_disaster = counts.index[0] if not counts.empty else "N/A"

    today_str = datetime.now().strftime("%Y-%m-%d")
    today_count = len(df[df["date"] == today_str]) if "date" in df.columns else 0

    return {
        "total_images": total_images,
        "avg_processing_time": avg_processing_time,
        "avg_affected_area": avg_affected_area,
        "most_common_disaster": most_common_disaster,
        "today_count": today_count
    }

def create_disaster_distribution_chart(history):
    """Generates Plotly Donut chart for disaster frequency distribution."""
    if not PLOTLY_AVAILABLE or not history:
        return None

    df = pd.DataFrame(history)
    counts = df["disaster_type"].value_counts().reset_index()
    counts.columns = ["disaster_type", "count"]

    color_discrete_map = {
        "Wildfire": "#DC2626",
        "Flood": "#2563EB",
        "Deforestation": "#059669",
        "Urban Expansion": "#8B5CF6",
        "Normal": "#10B981"
    }

    fig = px.pie(
        counts,
        values="count",
        names="disaster_type",
        hole=0.45,
        title="Disaster Class Distribution",
        color="disaster_type",
        color_discrete_map=color_discrete_map
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def create_severity_distribution_chart(history):
    """Generates Plotly Bar chart for severity breakdown across hazards."""
    if not PLOTLY_AVAILABLE or not history:
        return None

    df = pd.DataFrame(history)
    severity_counts = df.groupby(["disaster_type", "severity"]).size().reset_index(name="count")

    color_map = {
        "High": "#EF4444",
        "Medium": "#F59E0B",
        "Low": "#10B981"
    }

    fig = px.bar(
        severity_counts,
        x="disaster_type",
        y="count",
        color="severity",
        title="Severity Grade Breakdown by Disaster Type",
        color_discrete_map=color_map,
        barmode="stack"
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Disaster Category",
        yaxis_title="Image Count",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def create_affected_area_timeline_chart(history):
    """Generates Plotly scatter timeline tracking affected area % over analyses."""
    if not PLOTLY_AVAILABLE or not history:
        return None

    df = pd.DataFrame(history)
    df["index"] = range(len(df), 0, -1)  # Chronological order

    fig = px.line(
        df,
        x="timestamp",
        y="affected_area",
        color="disaster_type",
        markers=True,
        title="Affected Area % Trend Over Time"
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Timestamp",
        yaxis_title="Affected Area (%)",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig
