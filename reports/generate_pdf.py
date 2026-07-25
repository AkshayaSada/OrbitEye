import os
import io
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

def create_pdf_report(disaster_type, confidence, severity, affected_area, processing_time, explainability_text):
    """
    Generates a printable PDF report for the satellite disaster analysis.
    Returns bytes buffer of the PDF file.
    """
    if not REPORTLAB_AVAILABLE:
        # Text summary fallback if reportlab is not yet installed in local python environment
        text_content = f"OrbitEye Executive Disaster Intelligence Report\nTarget: {disaster_type}\nConfidence: {confidence:.1f}%\nSeverity: {severity}\nAffected Area: {affected_area:.1f}%\nProc Time: {processing_time}s\nExplainability: {explainability_text}"
        return text_content.encode('utf-8')

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#6B7280"),
        spaceAfter=15
    )
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1E40AF"),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1F2937")
    )

    story = []

    # Header Title
    story.append(Paragraph("OrbitEye 🌍 Earth Observation Intelligence", title_style))
    story.append(Paragraph(f"Automated Satellite Disaster Assessment Report — Reference ID: ORB-{datetime.now().strftime('%Y%m%d%H%M%S')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceAfter=15))

    # Metric Table Summary
    table_data = [
        [Paragraph("<b>Metric</b>", body_style), Paragraph("<b>Value / Details</b>", body_style)],
        [Paragraph("<b>Target Disaster Class</b>", body_style), Paragraph(f"<font color='#2563EB'><b>{disaster_type}</b></font>", body_style)],
        [Paragraph("<b>Model Confidence Score</b>", body_style), Paragraph(f"{confidence:.1f}%", body_style)],
        [Paragraph("<b>Affected Area Estimation</b>", body_style), Paragraph(f"<b>{affected_area:.1f}%</b> of total image sector", body_style)],
        [Paragraph("<b>Assessed Severity Grade</b>", body_style), Paragraph(f"<b>{severity}</b>", body_style)],
        [Paragraph("<b>Inference Processing Time</b>", body_style), Paragraph(f"{processing_time:.3f} seconds", body_style)],
        [Paragraph("<b>Analysis Timestamp</b>", body_style), Paragraph(datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"), body_style)]
    ]

    t = Table(table_data, colWidths=[200, 320])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor("#F3F4F6")),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.HexColor("#1F2937")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    # AI Explainability Section
    story.append(Paragraph("AI Model Explainability & Spectral Analysis", section_heading))
    story.append(Paragraph(explainability_text, body_style))
    story.append(Spacer(1, 10))

    # Causes & Impact Section
    causes_impact = _get_causes_and_impact(disaster_type)
    story.append(Paragraph("Possible Root Causes", section_heading))
    story.append(Paragraph(causes_impact["causes"], body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Potential Environmental & Social Impact", section_heading))
    story.append(Paragraph(causes_impact["impact"], body_style))
    story.append(Spacer(1, 10))

    # Emergency Guidance Protocols
    story.append(Paragraph("Recommended Emergency Response Actions", section_heading))
    story.append(Paragraph(causes_impact["actions"], body_style))
    story.append(Spacer(1, 20))

    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#9CA3AF"), spaceBefore=10, spaceAfter=10))
    story.append(Paragraph("Report generated automatically by OrbitEye AI Platform. Data verified via MobileNetV2 Earth Observation Engine.", subtitle_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def _get_causes_and_impact(disaster_type):
    """Utility providing disaster-specific causes, impacts, and actions for PDF generation."""
    data = {
        "Wildfire": {
            "causes": "Prolonged dry spells, high ambient temperatures, dry lightning, or human agricultural clearing activity.",
            "impact": "Severe thermal radiation, destruction of forest ecosystems, air quality degradation via PM2.5 particulate emissions, and wildlife habitat displacement.",
            "actions": "1. Deploy aerial firefighting units to perimeter containment lines.<br/>2. Issue immediate mandatory evacuation orders for downwind residential communities.<br/>3. Establish emergency smoke shelters and respiratory supply stations."
        },
        "Flood": {
            "causes": "Monsoonal heavy precipitation, riverbank overtopping, hurricane storm surges, or rapid snowpack melting.",
            "impact": "Submersion of arable cropland, structural damage to transportation corridors, contamination of drinking water reservoirs, and vector-borne disease risks.",
            "actions": "1. Evacuate low-lying riverine sectors immediately.<br/>2. Deploy inflatable rescue boats and sandbag barriers along secondary levees.<br/>3. Issue boil-water advisories and activate regional crisis shelters."
        },
        "Deforestation": {
            "causes": "Unregulated logging, commercial agricultural clear-cutting, mining operations, or road infrastructure expansion.",
            "impact": "Loss of natural carbon sinks, accelerated soil erosion, disruption of regional hydrological cycles, and biodiversity loss.",
            "actions": "1. Dispatch environmental enforcement patrols to stop unpermitted machinery.<br/>2. Implement immediate buffer-zone protections around vulnerable primary forest.<br/>3. Initiate reforestation and soil stabilization protocols."
        },
        "Urban Expansion": {
            "causes": "Rapid demographic urbanization, industrial park development, and commercial transportation network construction.",
            "impact": "Conversion of fertile agricultural land to impervious surfaces, creation of urban heat islands, and increased surface stormwater runoff.",
            "actions": "1. Enforce sustainable urban boundary zoning regulations.<br/>2. Mandate green rooftop and permeable pavement construction standards.<br/>3. Preserve contiguous urban green corridors and parklands."
        },
        "Normal": {
            "causes": "Stable seasonal meteorological conditions and sustainable land management practices.",
            "impact": "Sustained canopy photosynthesis, stable soil retention, and normal hydrological cycles.",
            "actions": "1. Continue routine satellite monitoring cycles.<br/>2. Maintain active baseline spectral logging for early anomaly detection."
        }
    }
    return data.get(disaster_type, data["Normal"])
