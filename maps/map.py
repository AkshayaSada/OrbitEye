try:
    import folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

DEMO_COORDINATES = {
    "Wildfire": (37.7749, -122.4194, "California Fire Sector, USA"),
    "Flood": (9.9312, 76.2673, "Kerala Inundated Basin, India"),
    "Deforestation": (-3.4653, -62.2159, "Amazon Basin Sector, Brazil"),
    "Urban Expansion": (35.6762, 139.6503, "Tokyo Metropolitan Rim, Japan"),
    "Normal": (46.8182, 8.2275, "Alpine Forest Sector, Switzerland")
}

def generate_disaster_map(lat=None, lon=None, disaster_type="Normal", severity="Low", affected_area=0.0):
    """
    Creates an interactive Folium map with satellite tiles, spatial markers, and affected risk radius.
    Returns folium.Map object or None if folium is uninstalled.
    """
    if not FOLIUM_AVAILABLE:
        return None

    if lat is None or lon is None:
        demo = DEMO_COORDINATES.get(disaster_type, DEMO_COORDINATES["Normal"])
        lat, lon, location_name = demo[0], demo[1], demo[2]
    else:
        location_name = f"Extracted EXIF Location ({lat:.4f}, {lon:.4f})"

    # Color mapping
    severity_colors = {
        "High": "#EF4444",
        "Medium": "#F59E0B",
        "Low": "#10B981"
    }
    color_hex = severity_colors.get(severity, "#3B82F6")

    # Base Folium Map centered on location
    m = folium.Map(location=[lat, lon], zoom_start=11, tiles=None)

    # Satellite & OpenStreetMap Tile Layers
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Satellite Imagery",
        overlay=False,
        control=True
    ).add_to(m)

    folium.TileLayer(
        tiles="OpenStreetMap",
        name="Standard Street Map",
        overlay=False,
        control=True
    ).add_to(m)

    # Disaster Marker Popup HTML
    popup_html = f"""
    <div style="font-family: Arial, sans-serif; width: 210px; padding: 4px;">
        <h4 style="margin: 0 0 6px 0; color: #1E3A8A;">OrbitEye Satellite Marker</h4>
        <hr style="margin: 4px 0; border-top: 1px solid #E5E7EB;">
        <b>Target Class:</b> {disaster_type}<br>
        <b>Affected Area:</b> {affected_area:.1f}%<br>
        <b>Severity:</b> <span style="color: {color_hex}; font-weight: bold;">{severity}</span><br>
        <span style="font-size: 11px; color: #6B7280;">Sector: {location_name}</span>
    </div>
    """

    # Custom Marker Icon
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=f"{disaster_type} ({severity} Severity)",
        icon=folium.Icon(color="red" if severity == "High" else ("orange" if severity == "Medium" else "green"), icon="info-sign")
    ).add_to(m)

    # Risk Circle Overlay (Radius scaled by affected_area %)
    radius_meters = max(500, int(affected_area * 150))
    folium.Circle(
        location=[lat, lon],
        radius=radius_meters,
        color=color_hex,
        fill=True,
        fill_color=color_hex,
        fill_opacity=0.35,
        popup=f"Impact Radius: ~{radius_meters}m"
    ).add_to(m)

    folium.LayerControl().add_to(m)
    return m
