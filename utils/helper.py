import os
import json
import time
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard", "history.json")

def load_history():
    """Load analysis history from history.json."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_history_entry(disaster_type, confidence, severity, affected_area, processing_time, image_name="uploaded_satellite.jpg"):
    """Append a new analysis record to history.json."""
    history = load_history()
    new_entry = {
        "id": len(history) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "image_name": image_name,
        "disaster_type": disaster_type,
        "confidence": round(float(confidence), 2),
        "severity": severity,
        "affected_area": round(float(affected_area), 1),
        "processing_time": round(float(processing_time), 3)
    }
    history.insert(0, new_entry)  # Newest first
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)
    return new_entry

def get_severity_color(severity):
    """Return color hex code for a severity grade."""
    mapping = {
        "High": "#EF4444",      # Red
        "Medium": "#F59E0B",    # Amber
        "Low": "#10B981"        # Emerald
    }
    return mapping.get(severity, "#6B7280")

def get_class_color(disaster_type):
    """Return theme color for disaster types."""
    mapping = {
        "Wildfire": "#DC2626",
        "Flood": "#2563EB",
        "Deforestation": "#059669",
        "Urban Expansion": "#8B5CF6",
        "Normal": "#10B981"
    }
    return mapping.get(disaster_type, "#3B82F6")
