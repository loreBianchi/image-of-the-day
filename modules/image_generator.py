import requests
import base64
from config import SD_API_URL, STEPS, WIDTH, HEIGHT
import os

def generate_image(prompt, filename="output.png"):
    payload = {
        "prompt": prompt, 
        "steps": STEPS, 
        "width": WIDTH, 
        "height": HEIGHT, 
        "cfg_scale": 7, 
        "sampler_name": "DPM++ 2M Karras",
        "negative_prompt": "blurry, distorted, low quality, text, watermark, logo, out of frame"
    }
    response = requests.post(SD_API_URL, json=payload).json()
    if response.get("images"):
        image_base64 = response["images"][0]
        image_bytes = base64.b64decode(image_base64)
    
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as f:
            f.write(image_bytes)
        return filename
    else:
        raise Exception("Errore nella generazione dell'immagine: " + str(response))
