# app.py
import os, sqlite3
from datetime import datetime
from flask import Flask, render_template, request, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

APP_ROOT = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(APP_ROOT, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
DB_PATH = os.path.join(APP_ROOT, "database.db")
MODEL_PATH = os.path.join(APP_ROOT, "model.h5")

# Load model
if not os.path.exists(MODEL_PATH):
    raise SystemExit("model.h5 not found. Place it in project root.")
model = load_model(MODEL_PATH)

# Replace with training label order
EMOTION_LABELS = ['Angry','Disgust','Fear','Happy','Sad','Surprise','Neutral']

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, email TEXT, age INTEGER,
        image_path TEXT, emotion TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit(); conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name','')
    email = request.form.get('email','')
    age = request.form.get('age','')
    file = request.files.get('photo')
    if not file:
        return "No file uploaded", 400
    fname = datetime.utcnow().strftime("%Y%m%d%H%M%S_") + file.filename.replace(" ", "_")
    save_path = os.path.join(UPLOAD_FOLDER, fname)
    file.save(save_path)
    # preprocess
    img = image.load_img(save_path, target_size=(48,48), color_mode='grayscale')
    arr = image.img_to_array(img)
    arr = np.expand_dims(arr, axis=0) / 255.0
    preds = model.predict(arr)
    emotion = EMOTION_LABELS[int(np.argmax(preds))]
    # store
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute('INSERT INTO users (name,email,age,image_path,emotion) VALUES (?,?,?,?,?)',
              (name,email,int(age) if age.isdigit() else None, os.path.relpath(save_path, APP_ROOT), emotion))
    conn.commit(); conn.close()
    return render_template('result.html', name=name, emotion=emotion, image_url=url_for('static', filename=f'uploads/{fname}'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
