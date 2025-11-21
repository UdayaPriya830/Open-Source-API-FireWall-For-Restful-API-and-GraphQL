import joblib
import numpy as np
import os
from typing import Dict, Any

MODEL_PATH = "firewall_anomaly_model.pkl"

def load_model():
    """Load ML model if available."""
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            return None
    return None

model = load_model()

def extract_features(request_data: Dict[str, Any]) -> np.ndarray:
    """Extract features from request data for ML analysis."""
    features = [
        len(request_data.get('body', '')),  # Body length
        len(request_data.get('url', '')),   # URL length
        request_data.get('status_code', 200),  # Status code
        1 if request_data.get('threat_type') != 'None' else 0,  # Is threat
        len(request_data.get('headers', {})),  # Header count
    ]
    return np.array([features])

def detect_anomaly(request_data: Dict[str, Any]) -> str:
    """Detect anomalies using ML model."""
    if model is None:
        return "ML Model Not Available"
    
    try:
        features = extract_features(request_data)
        prediction = model.predict(features)
        return "Anomaly Detected" if prediction[0] == -1 else "Normal"
    except Exception as e:
        return f"ML Error: {str(e)[:30]}"

def get_anomaly_score(request_data: Dict[str, Any]) -> float:
    """Get anomaly score (0-1, higher = more anomalous)."""
    if model is None or not hasattr(model, 'decision_function'):
        return 0.0
    
    try:
        features = extract_features(request_data)
        score = model.decision_function(features)[0]
        # Normalize to 0-1 range
        return max(0, min(1, (score + 1) / 2))
    except Exception:
        return 0.0
