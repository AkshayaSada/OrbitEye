import numpy as np
import cv2
from PIL import Image

def perform_change_detection(img_a, img_b):
    """
    Performs pixel-difference change detection between Image A (Baseline) and Image B (Post-Event).
    Returns:
    - delta_percentage: float (% pixel area changed)
    - change_summary: human readable summary text
    - diff_heatmap_pil: PIL Image visual heatmap of change locations
    """
    arr_a = np.array(img_a.convert("RGB").resize((224, 224)))
    arr_b = np.array(img_b.convert("RGB").resize((224, 224)))

    # Compute absolute RGB difference
    diff = cv2.absdiff(arr_a, arr_b)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)

    # Threshold significant changes (pixel delta > 30)
    _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
    
    total_pixels = 224 * 224
    changed_pixels = np.count_nonzero(thresh)
    delta_percentage = round((changed_pixels / total_pixels) * 100.0, 1)

    # Spectral shift analysis (Green canopy vs Blue water vs Gray urban)
    hsv_a = cv2.cvtColor(arr_a, cv2.COLOR_RGB2HSV)
    hsv_b = cv2.cvtColor(arr_b, cv2.COLOR_RGB2HSV)

    # Green canopy mask
    green_mask_a = cv2.inRange(hsv_a, np.array([35, 40, 40]), np.array([85, 255, 255]))
    green_mask_b = cv2.inRange(hsv_b, np.array([35, 40, 40]), np.array([85, 255, 255]))
    green_delta = (np.count_nonzero(green_mask_b) - np.count_nonzero(green_mask_a)) / total_pixels * 100.0

    # Blue water mask
    blue_mask_a = cv2.inRange(hsv_a, np.array([90, 50, 50]), np.array([140, 255, 255]))
    blue_mask_b = cv2.inRange(hsv_b, np.array([90, 50, 50]), np.array([140, 255, 255]))
    blue_delta = (np.count_nonzero(blue_mask_b) - np.count_nonzero(blue_mask_a)) / total_pixels * 100.0

    # Formulate change summary text
    if blue_delta > 10.0:
        change_summary = f"Flood expansion detected: +{abs(blue_delta):.1f}% increase in water surface area."
    elif green_delta < -10.0:
        change_summary = f"Deforestation / Canopy loss detected: {abs(green_delta):.1f}% reduction in green vegetation."
    elif delta_percentage > 15.0:
        change_summary = f"Urban Expansion / Infrastructure change detected: {delta_percentage:.1f}% land area modified."
    else:
        change_summary = f"Minor environmental change detected: {delta_percentage:.1f}% pixel variance."

    # Create Jet heatmap visualization
    heatmap = cv2.applyColorMap(gray_diff, cv2.COLORMAP_JET)
    blended = cv2.addWeighted(arr_b, 0.6, cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB), 0.4, 0)
    diff_heatmap_pil = Image.fromarray(blended)

    return delta_percentage, change_summary, diff_heatmap_pil
