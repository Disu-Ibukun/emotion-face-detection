import os
from flask import Flask, request, render_template, jsonify
from keras.models import load_model
import download_model  # this will download model.h5 if it doesn't exist

app = Flask(__name__)

# Ensure model.h5 exists in project root
MODEL_PATH = "model.h5"
if not os.path.exists(MODEL_PATH):
    download_model.download()  # call a function in download_model.py to fetch model

# Load the Keras model
model = load_model(MODEL_PATH)

# Get the Render port or default to 5000
PORT = int(os.environ.get("PORT", 5000))

@app.route('/')
def home():
    return render_template("index.html")  # your HTML form file

@app.route('/submit', methods=['POST'])
def submit():
    # Example: handle uploaded image
    if 'photo' not in request.files:
        return "No file uploaded", 400
    photo = request.files['photo']
    # Save the photo temporarily
    photo_path = os.path.join("/tmp", photo.filename)
    photo.save(photo_path)

    # Here you would preprocess the image and run your model prediction
    # prediction = model.predict(preprocess(photo_path))

    # Example placeholder response
    result = {"prediction": "happy"}  # replace with actual prediction
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
