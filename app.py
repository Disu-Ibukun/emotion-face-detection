import os
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model

app = Flask(__name__)

MODEL_PATH = "model.h5"

# Ensure model exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"{MODEL_PATH} not found. Make sure download_model.py ran during build.")

# Load the model
model = load_model(MODEL_PATH)

@app.route("/")
def home():
    return "Emotion Detection App is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    input_data = data.get("input")

    if input_data is None:
        return jsonify({"error": "No input data provided"}), 400

    prediction = model.predict([input_data])
    return jsonify({"prediction": prediction.tolist()})

PORT = int(os.environ.get("PORT", 5000))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
