"""Flask web app for water chemical-safety predictions with simplified inputs."""

import logging
from pathlib import Path
import pickle

import pandas as pd
from flask import Flask, jsonify, render_template, request

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load model
MODEL_PATH = Path(__file__).with_name("water_safety_xgboost_model.pkl")
logger.info("Loading XGBoost Pipeline model from %s", MODEL_PATH)

try:
    with MODEL_PATH.open("rb") as model_file:
        model = pickle.load(model_file)
    logger.info("Model loaded successfully. Type: %s", type(model))
except Exception as e:
    logger.critical("Failed to load model file: %s", e)
    raise RuntimeError(f"Could not load model: {e}") from e

# All 20 features in the exact order expected by the model pipeline
FEATURES = [
    "aluminium", "ammonia", "arsenic", "barium", "cadmium", "chloramine",
    "chromium", "copper", "flouride", "bacteria", "viruses", "lead",
    "nitrates", "nitrites", "mercury", "perchlorate", "radium", "selenium",
    "silver", "uranium"
]

# Top 5 most important features that the user will input in the UI
REQUIRED_FEATURES = ["cadmium", "aluminium", "silver", "perchlorate", "arsenic"]

# Median values of the remaining 15 features to be filled automatically
FEATURE_MEDIANS = {
    "aluminium": 0.07,
    "ammonia": 14.13,
    "arsenic": 0.05,
    "barium": 1.19,
    "cadmium": 0.04,
    "chloramine": 0.53,
    "chromium": 0.09,
    "copper": 0.75,
    "flouride": 0.77,
    "bacteria": 0.22,
    "viruses": 0.008,
    "lead": 0.102,
    "nitrates": 9.93,
    "nitrites": 1.42,
    "mercury": 0.005,
    "perchlorate": 7.745,
    "radium": 2.41,
    "selenium": 0.05,
    "silver": 0.08,
    "uranium": 0.05
}

def parse_measurements(data):
    """Validate user inputs for key features and automatically fill the rest with medians."""
    values = {}
    
    # 1. Parse and validate the 5 required features from user input
    for feature in REQUIRED_FEATURES:
        raw_value = data.get(feature, "")
        if raw_value in (None, ""):
            raise ValueError(f"Please enter a value for {feature.replace('_', ' ')}.")
        try:
            values[feature] = float(raw_value)
        except (TypeError, ValueError) as error:
            raise ValueError(f"'{feature.replace('_', ' ')}' must be a valid number.") from error
            
    # 2. Automatically populate the other 15 features with their median values
    for feature in FEATURES:
        if feature not in REQUIRED_FEATURES:
            # If the client sent a value, use it; otherwise use the median default
            raw_value = data.get(feature, "")
            if raw_value not in (None, ""):
                try:
                    values[feature] = float(raw_value)
                except (TypeError, ValueError):
                    values[feature] = FEATURE_MEDIANS[feature]
            else:
                values[feature] = FEATURE_MEDIANS[feature]
                
    # Return as a DataFrame in the exact feature order expected by the model
    return pd.DataFrame([values], columns=FEATURES)

def predict(data):
    """Run pipeline prediction and format response."""
    measurements = parse_measurements(data)
    
    # Get prediction probability (index 1 represents Safe)
    safety_probability = float(model.predict_proba(measurements)[0][1])
    is_safe = safety_probability >= 0.5
    
    return {
        "is_safe": is_safe,
        "label": "Safe" if is_safe else "Not Safe",
        "probability": round(safety_probability * 100, 2),
    }

@app.route("/", methods=["GET"])
def index():
    """Render the dashboard page."""
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def api_predict():
    """JSON endpoint for prediction queries."""
    try:
        if request.is_json:
            data = request.get_json(silent=True) or {}
        else:
            data = request.form.to_dict()
            
        result = predict(data)
        logger.info("Prediction successful: %s (Prob: %s%%)", result["label"], result["probability"])
        return jsonify(result)
    except ValueError as exc:
        logger.warning("Validation error during prediction: %s", exc)
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        logger.exception("Unexpected error during prediction")
        return jsonify({"error": "An unexpected error occurred processing your request."}), 500

if __name__ == "__main__":
    logger.info("Starting Flask application...")
    app.run(debug=True, host="http://127.0.0.1:5000", port=5000)
