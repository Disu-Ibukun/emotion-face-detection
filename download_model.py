import requests
import os

def download():
    url = "https://drive.google.com/uc?export=download&id=12loWK8x0TFpiatoNqfDTD6BGZPNcgSYN"
    model_path = "model.h5"

    if os.path.exists(model_path):
        print("model.h5 already exists, skipping download.")
        return

    print("Downloading model.h5...")
    r = requests.get(url, stream=True)
    with open(model_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Downloaded model.h5")
