"""
TruthLens - Flask API Server
Serves the Naive Bayes fake news detection model via REST endpoints.
"""

import os
import json
import joblib
import random

from flask import Flask, request, jsonify
from flask_cors import CORS

from model.lstm_model import NaiveBayesClassifier
from model.preprocess import TextPreprocessor

app = Flask(__name__)
CORS(app)

# Global references
model = None
preprocessor = TextPreprocessor()

# Paths
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'saved_model')

MODEL_PATH = os.path.join(MODEL_DIR, 'naive_bayes.pkl')

VECTORIZER_PATH = os.path.join(MODEL_DIR, 'tfidf.pkl')

METRICS_PATH = os.path.join(MODEL_DIR, 'metrics.json')


def load_model():
    """
    Load trained Naive Bayes model and TF-IDF vectorizer.
    """

    global model

    if not os.path.exists(MODEL_PATH):
        print("[WARNING] No trained model found.")
        print("Run 'python train.py' first.")
        return False

    model = NaiveBayesClassifier()

    model.load(MODEL_PATH, VECTORIZER_PATH)

    print("[INFO] Naive Bayes model loaded successfully.")

    return True


def demo_predict(text: str) -> dict:
    """
    Simulated prediction for demo mode.
    """

    steps = preprocessor.get_preprocessing_steps(text)

    fake_keywords = [
        'breaking',
        'shocking',
        'secret',
        'exposed',
        'viral',
        'hoax',
        'conspiracy',
        'urgent',
        'scam',
        'miracle',
        'banned'
    ]

    text_lower = text.lower()

    fake_score = 0

    for word in fake_keywords:
        if word in text_lower:
            fake_score += 0.12

    random.seed(hash(text) % 2**32)

    base = random.uniform(0.35, 0.65)

    probability_fake = min(max(base + fake_score, 0.05), 0.95)

    probability_real = 1 - probability_fake

    # Prediction logic
    if probability_fake >= 0.80:
        prediction = "FAKE"
        confidence = probability_fake

    elif probability_real >= 0.80:
        prediction = "REAL"
        confidence = probability_real

    else:
        prediction = "SUSPICIOUS"
        confidence = max(probability_fake, probability_real)

    return {
        "prediction": prediction,

        "confidence":
            round(float(confidence) * 100, 2),

        "probability_fake":
            round(float(probability_fake) * 100, 2),

        "probability_real":
            round(float(probability_real) * 100, 2),

        "preprocessing_steps": steps,

        "model_used": "demo_naive_bayes",

        "note":
            "Demo mode - train the model using python train.py"
    }


@app.route('/api/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    """

    return jsonify({
        "status": "healthy",

        "model_loaded": model is not None,

        "model_type": "Naive Bayes"
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict whether news text is REAL or FAKE.
    """

    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({
            "error": "Missing 'text' field"
        }), 400

    text = data['text'].strip()

    if len(text) < 20:
        return jsonify({
            "error":
                "Text too short. Minimum 20 characters required."
        }), 400

    # Demo mode
    if model is None:
        return jsonify(demo_predict(text))

    try:

        # Preprocess
        processed_text = preprocessor.preprocess(text)

        steps = preprocessor.get_preprocessing_steps(text)

        # Get probabilities
        probabilities = model.predict_proba([processed_text])[0]

        probability_real = float(probabilities[0])

        probability_fake = float(probabilities[1])

        # Confidence threshold logic
        if probability_fake >= 0.80:

            prediction = "FAKE"

            confidence = probability_fake

        elif probability_real >= 0.80:

            prediction = "REAL"

            confidence = probability_real

        else:

            prediction = "SUSPICIOUS"

            confidence = max(probability_fake, probability_real)

        return jsonify({

            "prediction": prediction,

            "confidence":
                round(confidence * 100, 2),

            "probability_fake":
                round(probability_fake * 100, 2),

            "probability_real":
                round(probability_real * 100, 2),

            "preprocessing_steps": steps,

            "model_used": "naive_bayes"

        })

    except Exception as e:

        return jsonify({
            "error": f"Prediction failed: {str(e)}"
        }), 500


@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """
    Return saved model metrics.
    """

    if os.path.exists(METRICS_PATH):

        with open(METRICS_PATH, 'r') as f:

            metrics = json.load(f)

        return jsonify(metrics)

    return jsonify({
        "error": "Metrics file not found"
    })


@app.route('/api/training-history', methods=['GET'])
def get_training_history():
    """
    Simulated training history for frontend charts.
    """

    history = {

        "epochs": list(range(1, 11)),

        "train_accuracy": [
            68.2,
            74.1,
            79.5,
            83.8,
            87.2,
            89.1,
            90.4,
            91.2,
            92.0,
            92.6
        ],

        "val_accuracy": [
            65.1,
            72.4,
            77.3,
            81.6,
            85.4,
            87.1,
            88.3,
            89.0,
            89.4,
            89.8
        ],

        "train_loss": [
            0.68,
            0.57,
            0.49,
            0.42,
            0.36,
            0.31,
            0.28,
            0.24,
            0.22,
            0.20
        ],

        "val_loss": [
            0.71,
            0.61,
            0.53,
            0.47,
            0.41,
            0.38,
            0.35,
            0.33,
            0.31,
            0.29
        ],

        "mode": "naive_bayes"
    }

    return jsonify(history)


if __name__ == '__main__':

    print("=" * 60)
    print(" TruthLens — Naive Bayes Fake News Detection")
    print("=" * 60)

    model_loaded = load_model()

    if not model_loaded:

        print("\n Starting in DEMO mode")
        print(" Train model using: python train.py\n")

    print(" Server: http://localhost:5000")

    print("=" * 60)

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False
    )