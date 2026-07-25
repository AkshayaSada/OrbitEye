import os
import io
import numpy as np
from PIL import Image, ExifTags

MAX_FILE_SIZE_MB = 50
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

def validate_image(uploaded_file):
    """Validates uploaded image file format and size."""
    if uploaded_file is None:
        return False, "No file uploaded."

    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Invalid file format '{ext}'. Allowed: JPG, PNG, TIFF."

    # Check file size
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        return False, f"File size exceeds {MAX_FILE_SIZE_MB} MB limit ({file_size_mb:.1f} MB)."

    return True, "File valid."

def preprocess_image(image_input, target_size=(224, 224)):
    """
    Reads image, converts to RGB, resizes to target_size, and returns:
    1. PIL Image object (224x224)
    2. Normalized NumPy array shape (1, 224, 224, 3) for MobileNetV2
    """
    if isinstance(image_input, (str, os.PathLike)):
        pil_img = Image.open(image_input).convert("RGB")
    elif isinstance(image_input, bytes):
        pil_img = Image.open(io.BytesIO(image_input)).convert("RGB")
    elif hasattr(image_input, "read"):
        image_input.seek(0)
        pil_img = Image.open(io.BytesIO(image_input.read())).convert("RGB")
    elif isinstance(image_input, Image.Image):
        pil_img = image_input.convert("RGB")
    else:
        raise ValueError("Unsupported image input type.")

    resized_img = pil_img.resize(target_size)
    img_array = np.array(resized_img, dtype=np.float32) / 255.0  # Normalize to [0, 1]
    tensor_input = np.expand_dims(img_array, axis=0)              # Add batch dimension

    return resized_img, tensor_input

def extract_exif_gps(image_input):
    """Extracts latitude & longitude coordinates from image EXIF metadata if present."""
    try:
        if isinstance(image_input, (str, os.PathLike)):
            img = Image.open(image_input)
        elif hasattr(image_input, "read"):
            image_input.seek(0)
            img = Image.open(io.BytesIO(image_input.read()))
        elif isinstance(image_input, Image.Image):
            img = image_input
        else:
            return None, None

        exif = img._getexif()
        if not exif:
            return None, None

        gps_info = {}
        for key, val in exif.items():
            if key in ExifTags.TAGS and ExifTags.TAGS[key] == "GPSInfo":
                for gps_key in val:
                    sub_tag = ExifTags.GPSTAGS.get(gps_key, gps_key)
                    gps_info[sub_tag] = val[gps_key]

        if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
            lat = _convert_to_degrees(gps_info["GPSLatitude"])
            if gps_info.get("GPSLatitudeRef") == "S":
                lat = -lat

            lon = _convert_to_degrees(gps_info["GPSLongitude"])
            if gps_info.get("GPSLongitudeRef") == "W":
                lon = -lon

            return lat, lon

    except Exception:
        pass

    return None, None

def _convert_to_degrees(value):
    """Helper to convert GPS EXIF coordinates to degrees float."""
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)
