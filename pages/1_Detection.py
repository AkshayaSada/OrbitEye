import streamlit as st
import os
import sys
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.theme import apply_phosphor_theme
from preprocessing.preprocess import validate_image, preprocess_image, extract_exif_gps
from preprocessing.severity import calculate_affected_area
from preprocessing.change_detection import perform_change_detection
from model.predict import predict_disaster
from reports.generate_pdf import create_pdf_report
from maps.map import generate_disaster_map
from emergency.response import get_emergency_protocol
from utils.helper import save_history_entry
from utils.demo_samples import ensure_sample_images
from streamlit_folium import st_folium

st.set_page_config(page_title="OrbitEye — Hazard Detection & Change Engine", page_icon="🔍", layout="wide")
apply_phosphor_theme()

st.markdown('<div class="eyebrow-tag">MODEL INFERENCE & CHANGE DETECTION</div>', unsafe_allow_html=True)
st.markdown("<h1 style='margin-bottom: 4px;'>Satellite Hazard Detection Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #7c8aa3; margin-bottom: 20px;'>MobileNetV2 Deep Learning Inference & Bi-Temporal Pixel Difference Analysis</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🛰️ Single Image Hazard Detection", "🔄 Bi-Temporal Change Detection"])

samples = ensure_sample_images()

# ----------------------------------------------------
# TAB 1: Single Image Hazard Detection
# ----------------------------------------------------
with tab1:
    col_up, col_btn = st.columns([3, 1])
    
    with col_up:
        uploaded_file = st.file_uploader(
            "Upload Satellite Imagery (JPG, PNG, TIFF — Max 50MB)",
            type=["jpg", "jpeg", "png", "tif", "tiff"],
            key="single_upload"
        )

    with col_btn:
        st.write("**Quick Demo Testing**")
        sample_choice = st.selectbox(
            "Try Sample Images:",
            ["Select...", "Wildfire Sample", "Flood Sample", "Deforestation Sample", "Urban Expansion Sample", "Normal Sample"]
        )

    active_img = None
    file_name = "uploaded_satellite.jpg"

    if uploaded_file is not None:
        valid, msg = validate_image(uploaded_file)
        if not valid:
            st.error(msg)
        else:
            active_img = Image.open(uploaded_file)
            file_name = uploaded_file.name
    elif sample_choice != "Select...":
        key_map = {
            "Wildfire Sample": "wildfire",
            "Flood Sample": "flood",
            "Deforestation Sample": "deforestation",
            "Urban Expansion Sample": "urban_expansion",
            "Normal Sample": "normal"
        }
        cls_key = key_map.get(sample_choice)
        if cls_key in samples:
            active_img = Image.open(samples[cls_key])
            file_name = f"sample_{cls_key}.jpg"

    if active_img is not None:
        st.divider()
        col_img, col_res = st.columns([1, 1])

        with col_img:
            st.subheader("🖼️ Preprocessed Satellite View")
            resized_pil, tensor_input = preprocess_image(active_img)
            st.image(resized_pil, caption="Resized to 224x224 RGB (Normalized)", use_container_width=True)

        with col_res:
            st.subheader("⚡ AI Classification & Severity")
            
            disaster_type, confidence, processing_time, explainability_text = predict_disaster(resized_pil)
            affected_area, severity, mask_overlay = calculate_affected_area(resized_pil, disaster_type)

            mcol1, mcol2, mcol3 = st.columns(3)
            with mcol1:
                st.markdown(f"""
                <div class="pipe-box">
                    <div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#4a5670;">TARGET HAZARD</div>
                    <div style="font-family:'Space Grotesk', sans-serif; font-size:22px; font-weight:700; color:#4ade80; margin-top:4px;">{disaster_type}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with mcol2:
                sev_class = "sev-chip-high" if severity == "High" else ("sev-chip-med" if severity == "Medium" else "sev-chip-low")
                st.markdown(f"""
                <div class="pipe-box">
                    <div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#4a5670;">AFFECTED AREA</div>
                    <div style="font-family:'Space Grotesk', sans-serif; font-size:22px; font-weight:700; color:#e7edf5; margin-top:4px;">{affected_area}%</div>
                    <div style="margin-top:4px;"><span class="{sev_class}">{severity}</span></div>
                </div>
                """, unsafe_allow_html=True)

            with mcol3:
                st.markdown(f"""
                <div class="pipe-box">
                    <div style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#4a5670;">PROC. TIME</div>
                    <div style="font-family:'Space Grotesk', sans-serif; font-size:22px; font-weight:700; color:#4ade80; margin-top:4px;">{processing_time}s</div>
                </div>
                """, unsafe_allow_html=True)

            st.write("")
            st.write("**Model Confidence Score**")
            st.progress(int(confidence) / 100.0, text=f"MobileNetV2 Confidence: {confidence:.1f}%")

            save_history_entry(disaster_type, confidence, severity, affected_area, processing_time, file_name)

        st.divider()

        # Explainability Section
        st.subheader("🧠 AI Explainability & Feature Mask")
        exp_col1, exp_col2 = st.columns([1, 1])
        with exp_col1:
            st.info(explainability_text)
            st.markdown(f"""
            <div class="orb-card">
                <div class="orb-card-title">Rule-Based Affected Area Rating</div>
                <div class="orb-card-desc">
                    Affected Pixel Share: <b>{affected_area}%</b><br>
                    Rules: &lt;20% Low | 20–50% Medium | &gt;50% High<br>
                    Resulting Severity Grade: <b>{severity}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with exp_col2:
            st.image(mask_overlay, caption="Spectral Feature Segmentation Overlay Mask", use_container_width=True)

        st.divider()

        # Spatial Map & Emergency Protocol
        st.subheader("📍 Spatial Mapping & Emergency Guidance")
        map_col, emergency_col = st.columns([1, 1])

        lat, lon = extract_exif_gps(active_img)
        with map_col:
            st.write("**Interactive Satellite Location Map**")
            folium_map = generate_disaster_map(lat, lon, disaster_type, severity, affected_area)
            if folium_map is not None:
                st_folium(folium_map, height=350, use_container_width=True)
            else:
                st.info("Interactive Map available when folium is installed.")

        with emergency_col:
            protocol = get_emergency_protocol(disaster_type)
            st.markdown(f"### {protocol['title']}")
            st.caption(protocol['summary'])
            
            with st.expander("📌 Safety Action Checklist", expanded=True):
                for item in protocol['instructions']:
                    st.write(f"- {item}")
            
            with st.expander("📞 Emergency Contacts"):
                for contact in protocol['hotlines']:
                    st.write(f"**{contact['service']}**: `{contact['number']}`")

        st.divider()

        # PDF Report Download
        st.subheader("📄 Export Executive Disaster Report")
        pdf_bytes = create_pdf_report(disaster_type, confidence, severity, affected_area, processing_time, explainability_text)
        st.download_button(
            label="📥 Download Official PDF Report",
            data=pdf_bytes,
            file_name=f"OrbitEye_Report_{disaster_type}_{severity}.pdf",
            mime="application/pdf"
        )

# ----------------------------------------------------
# TAB 2: Bi-Temporal Change Detection
# ----------------------------------------------------
with tab2:
    st.subheader("🔄 Bi-Temporal Before & After Pixel Difference Analysis")
    st.caption("Upload two satellite images captured over the same sector at different timestamps to calculate canopy loss, water spread, or urban growth.")

    col_a, col_b = st.columns(2)
    with col_a:
        file_a = st.file_uploader("Upload Image A (Baseline / Before)", type=["jpg", "png", "tif"], key="change_a")
    with col_b:
        file_b = st.file_uploader("Upload Image B (Post-Event / After)", type=["jpg", "png", "tif"], key="change_b")

    if file_a is None or file_b is None:
        st.info("💡 Tip: Upload Image A and Image B above, or use the pre-loaded sample comparison below.")
        img_a = Image.open(samples["normal"])
        img_b = Image.open(samples["deforestation"])
    else:
        img_a = Image.open(file_a)
        img_b = Image.open(file_b)

    st.write("---")
    dcol1, dcol2, dcol3 = st.columns(3)
    with dcol1:
        st.image(img_a, caption="Image A (Baseline Sector)", use_container_width=True)
    with dcol2:
        st.image(img_b, caption="Image B (Post-Event Sector)", use_container_width=True)
    
    delta_percentage, change_summary, diff_heatmap = perform_change_detection(img_a, img_b)
    
    with dcol3:
        st.image(diff_heatmap, caption="Pixel Difference Heatmap (JET)", use_container_width=True)

    st.success(f"**Quantified Change Result**: {change_summary}")
    st.metric("Total Pixel Delta Variance", f"{delta_percentage}%")
