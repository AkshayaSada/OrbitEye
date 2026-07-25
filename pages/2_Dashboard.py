import streamlit as st
import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.theme import apply_phosphor_theme
from utils.helper import load_history
from dashboard.analytics import (
    generate_dashboard_metrics,
    create_disaster_distribution_chart,
    create_severity_distribution_chart,
    create_affected_area_timeline_chart
)

st.set_page_config(page_title="OrbitEye — Analytics Dashboard", page_icon="📊", layout="wide")
apply_phosphor_theme()

st.markdown('<div class="eyebrow-tag">ANALYTICS DASHBOARD</div>', unsafe_allow_html=True)
st.markdown("<h1 style='margin-bottom: 4px;'>Earth Observation Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #7c8aa3; margin-bottom: 24px;'>Aggregated KPI Analytics & Historical Disaster Tracking</p>", unsafe_allow_html=True)

history = load_history()
metrics = generate_dashboard_metrics(history)

# KPI Cards Row
kcol1, kcol2, kcol3, kcol4, kcol5 = st.columns(5)

with kcol1:
    st.markdown(f"""
    <div class="pipe-box">
        <div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#4a5670;">IMAGES ANALYZED</div>
        <div style="font-family:'Space Grotesk', sans-serif; font-size:24px; font-weight:700; color:#e7edf5; margin-top:6px;">{metrics['total_images']}</div>
    </div>
    """, unsafe_allow_html=True)

with kcol2:
    st.markdown(f"""
    <div class="pipe-box">
        <div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#4a5670;">AVG LATENCY</div>
        <div style="font-family:'Space Grotesk', sans-serif; font-size:24px; font-weight:700; color:#4ade80; margin-top:6px;">{metrics['avg_processing_time']}s</div>
    </div>
    """, unsafe_allow_html=True)

with kcol3:
    st.markdown(f"""
    <div class="pipe-box">
        <div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#4a5670;">AVG AFFECTED AREA</div>
        <div style="font-family:'Space Grotesk', sans-serif; font-size:24px; font-weight:700; color:#fbbf24; margin-top:6px;">{metrics['avg_affected_area']}%</div>
    </div>
    """, unsafe_allow_html=True)

with kcol4:
    st.markdown(f"""
    <div class="pipe-box">
        <div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#4a5670;">MOST COMMON CLASS</div>
        <div style="font-family:'Space Grotesk', sans-serif; font-size:18px; font-weight:700; color:#4ade80; margin-top:6px;">{metrics['most_common_disaster']}</div>
    </div>
    """, unsafe_allow_html=True)

with kcol5:
    st.markdown(f"""
    <div class="pipe-box">
        <div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#4a5670;">TODAY'S SCANS</div>
        <div style="font-family:'Space Grotesk', sans-serif; font-size:24px; font-weight:700; color:#e7edf5; margin-top:6px;">{metrics['today_count']}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Charts Row 1
c1, c2 = st.columns(2)
with c1:
    fig_dist = create_disaster_distribution_chart(history)
    if fig_dist is not None:
        st.plotly_chart(fig_dist, use_container_width=True)
    else:
        st.info("Disaster Class Distribution Chart (Install plotly to render)")

with c2:
    fig_sev = create_severity_distribution_chart(history)
    if fig_sev is not None:
        st.plotly_chart(fig_sev, use_container_width=True)
    else:
        st.info("Severity Breakdown Chart (Install plotly to render)")

# Chart Row 2
fig_timeline = create_affected_area_timeline_chart(history)
if fig_timeline is not None:
    st.plotly_chart(fig_timeline, use_container_width=True)

st.divider()

# Recent Analyses Data Table
st.subheader("📋 Historical Analysis Registry")
if history:
    df_history = pd.DataFrame(history)
    st.dataframe(
        df_history[["id", "timestamp", "image_name", "disaster_type", "confidence", "severity", "affected_area", "processing_time"]],
        column_config={
            "id": "ID",
            "timestamp": "Timestamp",
            "image_name": "Image File",
            "disaster_type": "Disaster Class",
            "confidence": st.column_config.NumberColumn("Confidence (%)", format="%.1f%%"),
            "severity": "Severity Grade",
            "affected_area": st.column_config.NumberColumn("Affected Area (%)", format="%.1f%%"),
            "processing_time": st.column_config.NumberColumn("Proc. Time (s)", format="%.3fs")
        },
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No history entries logged yet.")
