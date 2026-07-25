import os
import sys
from PIL import Image

sys.path.append(os.path.dirname(__file__))

from utils.demo_samples import ensure_sample_images
from preprocessing.preprocess import preprocess_image
from model.predict import predict_disaster
from preprocessing.severity import calculate_affected_area
from preprocessing.change_detection import perform_change_detection
from reports.generate_pdf import create_pdf_report
from maps.map import generate_disaster_map
from emergency.response import get_emergency_protocol
from dashboard.analytics import generate_dashboard_metrics
from utils.helper import load_history, save_history_entry

def safe_str(text):
    """Encodes string safely for Windows console printing."""
    return str(text).encode('ascii', 'ignore').decode('ascii')

def run_tests():
    print("=========================================")
    print("  OrbitEye V1 Verification Test Suite    ")
    print("=========================================")
    
    # 1. Sample Images
    samples = ensure_sample_images()
    print(f"[OK] Sample Images ready: {list(samples.keys())}")
    
    # 2. Preprocessing & Prediction Test
    test_img = Image.open(samples["wildfire"])
    resized, tensor = preprocess_image(test_img)
    disaster_type, confidence, proc_time, exp_text = predict_disaster(resized)
    print(f"[OK] AI Prediction: Class={disaster_type}, Confidence={confidence}%, ProcTime={proc_time}s")
    print(f"  Explainability: {safe_str(exp_text)}")

    # 3. Affected Area Estimation
    aff_pct, severity, mask_img = calculate_affected_area(resized, disaster_type)
    print(f"[OK] Affected Area Estimation: {aff_pct}%, Severity={severity}")

    # 4. Bi-Temporal Change Detection
    img_a = Image.open(samples["normal"])
    img_b = Image.open(samples["deforestation"])
    delta_pct, summary, diff_img = perform_change_detection(img_a, img_b)
    print(f"[OK] Change Detection Delta: {delta_pct}% -> {safe_str(summary)}")

    # 5. PDF Generation Test
    pdf_bytes = create_pdf_report(disaster_type, confidence, severity, aff_pct, proc_time, exp_text)
    print(f"[OK] PDF Report generated: {len(pdf_bytes)} bytes")

    # 6. Map Generation Test
    folium_map = generate_disaster_map(None, None, disaster_type, severity, aff_pct)
    print(f"[OK] Folium Map generator evaluated")

    # 7. Emergency Protocols
    protocol = get_emergency_protocol(disaster_type)
    print(f"[OK] Emergency Protocol retrieved: {safe_str(protocol['title'])}")

    # 8. History & Analytics
    history = load_history()
    metrics = generate_dashboard_metrics(history)
    print(f"[OK] Dashboard Metrics: Total Images={metrics['total_images']}, Avg Time={metrics['avg_processing_time']}s")

    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
