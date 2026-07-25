import streamlit as st

def apply_phosphor_theme():
    """Injects the OrbitEye Phosphor Green Dark Glassmorphism CSS Design System into any Streamlit page."""
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --void: #090c13;
            --panel: #101623;
            --panel-2: #151d2e;
            --line: #202b3f;
            --phosphor: #4ade80;
            --phosphor-dim: #1f5c3c;
            --amber: #fbbf24;
            --alert: #f87171;
            --ink: #e7edf5;
            --ink-dim: #7c8aa3;
            --ink-faint: #4a5670;
            --display: 'Space Grotesk', sans-serif;
            --mono: 'JetBrains Mono', monospace;
            --body: 'Inter', sans-serif;
        }

        /* Streamlit Body & App Background */
        .stApp {
            background-color: #090c13 !important;
            background-image:
                linear-gradient(#202b3f 1px, transparent 1px),
                linear-gradient(90deg, #202b3f 1px, transparent 1px) !important;
            background-size: 64px 64px !important;
            color: #e7edf5 !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* Main Container Alignment */
        .main .block-container {
            max-width: 1240px !important;
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }

        /* Sidebar Theme */
        [data-testid="stSidebar"] {
            background-color: #101623 !important;
            border-right: 1px solid #202b3f !important;
        }
        [data-testid="stSidebar"] * {
            color: #e7edf5 !important;
        }

        /* Headings */
        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif !important;
            color: #e7edf5 !important;
            letter-spacing: -0.01em !important;
        }

        /* Subtitles & Monospace tags */
        .eyebrow-tag {
            font-family: 'JetBrains Mono', monospace;
            font-size: 11.5px;
            letter-spacing: 0.16em;
            color: #4ade80;
            text-transform: uppercase;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .eyebrow-tag::before {
            content: '';
            width: 16px;
            height: 1px;
            background: #4ade80;
        }

        /* Panel Cards */
        .orb-card {
            background: #101623;
            border: 1px solid #202b3f;
            border-radius: 6px;
            padding: 24px;
            margin-bottom: 16px;
            transition: all 0.2s ease;
        }
        .orb-card:hover {
            background: #151d2e;
            border-color: #4ade80;
        }

        .orb-card-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 17px;
            font-weight: 600;
            color: #e7edf5;
            margin-bottom: 8px;
        }
        .orb-card-desc {
            font-size: 13.5px;
            color: #7c8aa3;
            line-height: 1.6;
        }
        .orb-card-tag {
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            color: #4a5670;
            letter-spacing: 0.1em;
            margin-bottom: 10px;
        }

        /* Pipeline Steps */
        .pipe-box {
            background: #101623;
            border: 1px solid #202b3f;
            border-radius: 6px;
            padding: 20px;
            text-align: center;
            height: 100%;
        }
        .pipe-num {
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            color: #4ade80;
            border: 1px solid #1f5c3c;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 12px auto;
            background: #090c13;
        }

        /* Severity Chips */
        .sev-chip-low {
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            padding: 5px 12px;
            border-radius: 3px;
            color: #4ade80;
            border: 1px solid #1f5c3c;
            background: rgba(74, 222, 128, 0.05);
            font-weight: 600;
            display: inline-block;
        }
        .sev-chip-med {
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            padding: 5px 12px;
            border-radius: 3px;
            color: #fbbf24;
            border: 1px solid #6b5518;
            background: rgba(251, 191, 36, 0.05);
            font-weight: 600;
            display: inline-block;
        }
        .sev-chip-high {
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            padding: 5px 12px;
            border-radius: 3px;
            color: #f87171;
            border: 1px solid #6b2b28;
            background: rgba(248, 113, 113, 0.05);
            font-weight: 600;
            display: inline-block;
        }

        /* Buttons Styling */
        div.stButton > button:first-child {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 13px !important;
            background: #4ade80 !important;
            color: #06170f !important;
            border-radius: 4px !important;
            font-weight: 600 !important;
            padding: 10px 24px !important;
            border: none !important;
            transition: all 0.2s ease !important;
        }
        div.stButton > button:first-child:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px -8px rgba(74, 222, 128, 0.6) !important;
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #101623;
            padding: 6px;
            border-radius: 6px;
            border: 1px solid #202b3f;
        }
        .stTabs [data-baseweb="tab"] {
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            color: #7c8aa3;
            border-radius: 4px;
            padding: 8px 16px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #151d2e !important;
            color: #4ade80 !important;
            border: 1px solid #1f5c3c !important;
        }
    </style>
    """, unsafe_allow_html=True)
