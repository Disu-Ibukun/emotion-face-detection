import os
import requests

MODEL_PATH = "model.h5"
MODEL_URL = "https://drive.google.com/uc?export=download&id=12loWK8x0TFpiatoNqfDTD6BGZPNcgSYN"

def download_model(url=MODEL_URL, save_path=MODEL_PATH):
    if os.path.exists(save_path):
        print(f"{save_path} already exists, skipping download.")
        return

    print(f"Downloading model from {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print("Model downloaded successfully.")

if __name__ == "__main__":
    download_model()
