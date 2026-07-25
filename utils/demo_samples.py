import os
import numpy as np
from PIL import Image, ImageDraw

DATASET_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataset")

def ensure_sample_images():
    """Generates clean, representative sample satellite images for testing if absent."""
    classes = ["wildfire", "flood", "deforestation", "urban_expansion", "normal"]
    sample_files = {}

    for cls in classes:
        cls_dir = os.path.join(DATASET_DIR, cls)
        os.makedirs(cls_dir, exist_ok=True)
        img_path = os.path.join(cls_dir, f"sample_{cls}.jpg")

        if not os.path.exists(img_path):
            img = generate_synthetic_satellite_image(cls)
            img.save(img_path, quality=95)
        
        sample_files[cls] = img_path

    return sample_files

def generate_synthetic_satellite_image(disaster_type, size=(224, 224)):
    """Creates a high-contrast synthetic satellite texture for demonstration."""
    np.random.seed(42 + hash(disaster_type) % 100)
    width, height = size
    
    # Base terrain: Green canopy / soil
    base = np.zeros((height, width, 3), dtype=np.uint8)
    base[:, :, 0] = np.random.randint(30, 70, (height, width))   # R
    base[:, :, 1] = np.random.randint(100, 180, (height, width)) # G (Canopy)
    base[:, :, 2] = np.random.randint(30, 70, (height, width))   # B
    
    img = Image.fromarray(base)
    draw = ImageDraw.Draw(img)

    if disaster_type == "wildfire":
        # Intense red/orange active fire zones & black burn scars
        for _ in range(15):
            x1, y1 = np.random.randint(20, width-20), np.random.randint(20, height-20)
            r = np.random.randint(15, 45)
            draw.ellipse([x1-r, y1-r, x1+r, y1+r], fill=(240, 60, 20)) # Flame red
        for _ in range(10):
            x1, y1 = np.random.randint(20, width-20), np.random.randint(20, height-20)
            r = np.random.randint(10, 30)
            draw.ellipse([x1-r, y1-r, x1+r, y1+r], fill=(30, 20, 20)) # Burn scar

    elif disaster_type == "flood":
        # Broad blue river / inundated plain
        draw.polygon([(0, 40), (width, 80), (width, height-30), (0, height-70)], fill=(30, 90, 220))
        for _ in range(8):
            x1, y1 = np.random.randint(10, width-10), np.random.randint(10, height-10)
            r = np.random.randint(15, 35)
            draw.ellipse([x1-r, y1-r, x1+r, y1+r], fill=(20, 110, 230))

    elif disaster_type == "deforestation":
        # Brown patch clear-cutting inside green canopy
        draw.rectangle([30, 30, 180, 180], fill=(160, 120, 70))
        draw.polygon([(10, 10), (100, 20), (120, 150), (40, 190)], fill=(180, 140, 80))

    elif disaster_type == "urban_expansion":
        # Gray concrete grid & rooftop blocks
        draw.rectangle([0, 0, width, height], fill=(130, 150, 110)) # Transition terrain
        for x in range(10, width, 30):
            draw.line([(x, 0), (x, height)], fill=(200, 200, 205), width=4)
        for y in range(10, height, 30):
            draw.line([(0, y), (width, y)], fill=(200, 200, 205), width=4)
        for _ in range(25):
            x = np.random.randint(10, width-25)
            y = np.random.randint(10, height-25)
            draw.rectangle([x, y, x+18, y+18], fill=(220, 220, 230))

    elif disaster_type == "normal":
        # Healthy green forest & clear fields
        for _ in range(30):
            x1, y1 = np.random.randint(0, width), np.random.randint(0, height)
            r = np.random.randint(20, 50)
            draw.ellipse([x1-r, y1-r, x1+r, y1+r], fill=(20, np.random.randint(140, 210), 40))

    return img
