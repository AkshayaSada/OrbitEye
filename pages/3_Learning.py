import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.theme import apply_phosphor_theme

st.set_page_config(page_title="OrbitEye — Learning Hub", page_icon="🎓", layout="wide")
apply_phosphor_theme()

st.markdown('<div class="eyebrow-tag">EDUCATIONAL RESOURCE</div>', unsafe_allow_html=True)
st.markdown("<h1 style='margin-bottom: 4px;'>Earth Observation Learning Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #7c8aa3; margin-bottom: 24px;'>Satellite Imaging, Disaster Dynamics, and Spectral Index Mathematics</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="orb-card">
        <div class="orb-card-tag">CONCEPT_01</div>
        <div class="orb-card-title">🌊 What is Flood Inundation Mapping?</div>
        <div class="orb-card-desc">
            Flood inundation mapping uses satellite sensors to detect surface water expansion over normally dry land. 
            Because liquid water strongly absorbs Near-Infrared (NIR) light, flooded regions appear as dark or high-contrast blue patches in false-color composites.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔬 Deep Dive: Water Spectral Index (NDWI)"):
        st.latex(r"NDWI = \frac{Green - NIR}{Green + NIR}")
        st.write("""
        The Normalized Difference Water Index (NDWI) isolates open water bodies. Values above +0.2 indicate surface water inundation, helping emergency teams map flood boundaries through cloud cover using Synthetic Aperture Radar (SAR).
        """)

    st.markdown("""
    <div class="orb-card">
        <div class="orb-card-tag">CONCEPT_02</div>
        <div class="orb-card-title">🪵 What is Deforestation & Canopy Degradation?</div>
        <div class="orb-card-desc">
            Deforestation refers to the large-scale removal of forest canopy for agriculture, logging, or infrastructure. 
            Satellites identify clear-cutting by tracking sudden drops in chlorophyll absorption and increases in exposed soil reflectance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔬 Deep Dive: Forest Canopy Degradation Tracking"):
        st.write("""
        Continuous satellite monitoring compares multi-temporal greenness indices to flag illegal road opening and selective logging before complete clear-cutting occurs.
        """)

    st.markdown("""
    <div class="orb-card">
        <div class="orb-card-tag">CONCEPT_03</div>
        <div class="orb-card-title">🛰️ Optical vs. SAR Satellite Imaging</div>
        <div class="orb-card-desc">
            <b>Optical Sensors</b> capture reflected sunlight in visible (RGB) and infrared bands (e.g. Sentinel-2, Landsat).<br>
            <b>Synthetic Aperture Radar (SAR)</b> emits microwave pulses to pierce through clouds, rain, and darkness (e.g. Sentinel-1).
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="orb-card">
        <div class="orb-card-tag">CONCEPT_04</div>
        <div class="orb-card-title">🔥 What is Wildfire Thermal Detection?</div>
        <div class="orb-card-desc">
            Active wildfires emit intense thermal radiation in Short-Wave Infrared (SWIR) and thermal infrared bands. 
            Satellites measure flame temperature fronts (red/orange peak) and post-fire charcoal burn scars (black/brown deposits).
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔬 Deep Dive: Normalized Burn Ratio (NBR)"):
        st.latex(r"NBR = \frac{NIR - SWIR}{NIR + SWIR}")
        st.write("""
        The Normalized Burn Ratio (NBR) uses NIR (healthy canopy) and SWIR (burnt soil) to measure fire severity. Higher delta-NBR indicates severe ecological destruction.
        """)

    st.markdown("""
    <div class="orb-card">
        <div class="orb-card-tag">CONCEPT_05</div>
        <div class="orb-card-title">🏙️ What is Urban Expansion & Heat Island Effect?</div>
        <div class="orb-card-desc">
            Urban expansion converts permeable green fields into concrete, asphalt, and rooftops. 
            This increases surface thermal retention, creating "Urban Heat Islands" and amplifying urban stormwater runoff risks.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="orb-card">
        <div class="orb-card-tag">CONCEPT_06</div>
        <div class="orb-card-title">🌿 What is NDVI (Vegetation Index)?</div>
        <div class="orb-card-desc">
            The Normalized Difference Vegetation Index (NDVI) quantifies plant health by comparing Red light absorption (chlorophyll) with NIR reflection (cell structure).
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔬 Deep Dive: NDVI Mathematical Formula"):
        st.latex(r"NDVI = \frac{NIR - Red}{NIR + Red}")
        st.write("""
        - **NDVI = +0.6 to +0.9**: Dense, healthy forest canopy
        - **NDVI = +0.2 to +0.4**: Sparse vegetation / shrubland
        - **NDVI = 0.0 to +0.1**: Exposed rock, soil, or urban concrete
        - **NDVI < 0.0**: Water surface
        """)
