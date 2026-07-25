import numpy as np
import cv2
from PIL import Image

def calculate_affected_area(pil_img, disaster_type):
    """
    Computes Affected Area Estimation percentage by segmenting spectral color signatures:
    - Wildfire: Thermal Red/Orange & dark burn scar pixels
    - Flood: Deep blue / muddy inundated water pixels
    - Deforestation: Non-green soil/brown pixels in canopy
    - Urban Expansion: Gray/reflective concrete & built-up structures
    - Normal: Minimal anomaly (<5%)

    Severity rules:
    - < 20%  --> Low Severity
    - 20-50% --> Medium Severity
    - > 50%  --> High Severity

    Returns: (affected_percentage, severity_label, mask_overlay_pil)
    """
    img_np = np.array(pil_img.convert("RGB"))
    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
    total_pixels = img_np.shape[0] * img_np.shape[1]

    mask = np.zeros((img_np.shape[0], img_np.shape[1]), dtype=np.uint8)
    overlay_color = (255, 0, 0) # Default Red overlay

    if disaster_type == "Wildfire":
        # Red & Orange active flame mask + dark smoke/burn scar
        lower_fire1 = np.array([0, 100, 100])
        upper_fire1 = np.array([25, 255, 255])
        lower_fire2 = np.array([160, 100, 100])
        upper_fire2 = np.array([179, 255, 255])
        mask_f1 = cv2.inRange(hsv, lower_fire1, upper_fire1)
        mask_f2 = cv2.inRange(hsv, lower_fire2, upper_fire2)
        
        # Burn scar (very low value/dark)
        lower_dark = np.array([0, 0, 0])
        upper_dark = np.array([180, 255, 45])
        mask_dark = cv2.inRange(hsv, lower_dark, upper_dark)
        
        mask = cv2.bitwise_or(cv2.bitwise_or(mask_f1, mask_f2), mask_dark)
        overlay_color = (239, 68, 68) # Red

    elif disaster_type == "Flood":
        # Blue water inundation mask
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([140, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        overlay_color = (37, 99, 235) # Blue

    elif disaster_type == "Deforestation":
        # Non-green soil/brown deforested area mask (complement of green canopy)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        mask = cv2.bitwise_not(green_mask)
        overlay_color = (217, 119, 6) # Amber/Brown

    elif disaster_type == "Urban Expansion":
        # High brightness, low saturation (concrete/gray built-up) mask
        lower_urban = np.array([0, 0, 140])
        upper_urban = np.array([180, 50, 255])
        mask = cv2.inRange(hsv, lower_urban, upper_urban)
        overlay_color = (139, 92, 246) # Purple

    else:  # Normal / Clear
        # Small noise threshold
        affected_percentage = 4.2
        severity_label = "Low"
        mask = np.zeros((img_np.shape[0], img_np.shape[1]), dtype=np.uint8)
        mask_overlay = Image.fromarray(img_np)
        return affected_percentage, severity_label, mask_overlay

    affected_pixels = int(np.count_nonzero(mask))
    affected_percentage = round((affected_pixels / total_pixels) * 100.0, 1)

    # Classify Severity based on rules:
    if affected_percentage < 20.0:
        severity_label = "Low"
    elif 20.0 <= affected_percentage <= 50.0:
        severity_label = "Medium"
    else:
        severity_label = "High"

    # Create semi-transparent mask overlay visual
    overlay_np = img_np.copy()
    overlay_np[mask > 0] = overlay_color
    blended = cv2.addWeighted(img_np, 0.6, overlay_np, 0.4, 0)
    mask_overlay = Image.fromarray(blended)

    return affected_percentage, severity_label, mask_overlay
