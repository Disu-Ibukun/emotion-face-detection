# download_model.py
import requests

url = "https://drive.google.com/file/d/12loWK8x0TFpiatoNqfDTD6BGZPNcgSYN/view?usp=sharing"  

r = requests.get(url, stream=True)

with open("model.h5", "wb") as f:
    for chunk in r.iter_content(chunk_size=8192):
        f.write(chunk)

print("Downloaded model.h5")
