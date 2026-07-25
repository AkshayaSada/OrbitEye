import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.theme import apply_phosphor_theme

st.set_page_config(page_title="OrbitEye — About & Developer Profile", page_icon="👩🏻‍💻", layout="wide")
apply_phosphor_theme()

st.markdown('<div class="eyebrow-tag">DEVELOPER & RESEARCH</div>', unsafe_allow_html=True)
st.markdown("<h1 style='margin-bottom: 4px;'>About OrbitEye & Developer</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #7c8aa3; margin-bottom: 24px;'>Earth Observation Research & Machine Learning Architecture</p>", unsafe_allow_html=True)

col_p, col_info = st.columns([1, 2])

with col_p:
    st.markdown("""
    <div class="orb-card" style="text-align: center; padding: 28px;">
        <div style="width: 100px; height: 100px; border-radius: 50%; border: 2px solid #4ade80; margin: 0 auto 16px auto; background: #151d2e; display: flex; align-items: center; justify-content: center; font-size: 2.5rem;">
            👩🏻‍💻
        </div>
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; color: #e7edf5;">Akshaya Sadasivan</div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #4ade80; margin-top: 4px; margin-bottom: 12px;">AI / ML Engineer & EO Researcher</div>
        <p style="color: #7c8aa3; font-size: 13.5px; line-height: 1.5;">Specializing in Deep Learning, Computer Vision, and Geospatial Intelligence Systems.</p>
        <div style="margin-top: 16px;">
            <span class="sev-chip-low">Computer Vision</span>
            <span class="sev-chip-low">Remote Sensing</span>
            <span class="sev-chip-low">Disaster Monitoring</span>
            <span class="sev-chip-low">Transfer Learning</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_info:
    st.markdown("### 📖 Developer Bio & Vision")
    st.write("""
    I am an **Artificial Intelligence & Machine Learning (AIML)** researcher passionate about leveraging deep learning 
    to address real-world climate crises and emergency response challenges. 

    **OrbitEye** was conceived to bridge the gap between complex Earth Observation (EO) multispectral data and real-time field decision-making. 
    By applying MobileNetV2 transfer learning, spectral segmentations, and bi-temporal change detection, OrbitEye provides emergency command centers 
    with instant, verifiable disaster intelligence.
    """)

    st.divider()

    st.markdown("### 🎓 Research & Focus Areas")
    st.markdown("""
    - **Multispectral Satellite Analytics**: Processing Sentinel-2 and EuroSAT land-use imagery for disaster detection.
    - **Explainable AI (XAI)**: Rule-based spectral feature maps ensuring model predictions are interpretable for environmental authorities.
    - **Bi-Temporal Change Algorithms**: Quantifying deforestation and flood expansion with pixel-difference heatmaps.
    - **Scalable Web Intelligence Platforms**: Building reactive, high-performance Streamlit architectures.
    """)

    st.divider()

    st.markdown("### 🔗 Professional Connections & Resume")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("[🌐 **GitHub Profile**](https://github.com/AkshayaSada)")
    with c2:
        st.markdown("[💼 **LinkedIn Network**](https://www.linkedin.com/in/akshaya-sadasivan/)")
    with c3:
        with open("Akshaya_Sadasivan_Resume.pdf", "rb") as f:
            resume_data = f.read()
        st.download_button(
            label="📄 Download Resume",
            data=sample_resume_pdf,
            file_name="Akshaya_Sadasivan_Resume.pdf",
            mime="application/pdf"
        )
