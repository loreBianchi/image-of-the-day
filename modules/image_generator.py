import requests
import base64
from config import SD_URL, STEPS, WIDTH, HEIGHT, NEGATIVE_PROMPT, MODEL
import os
from datetime import datetime

def generate_image(prompt, output_path, width=WIDTH, height=HEIGHT):
    """
    Generate an image using Stable Diffusion API based on the given prompt.
    """
    payload = {
        "prompt": prompt,
        "negative_prompt": NEGATIVE_PROMPT,
        "steps": STEPS,
        "sampler_name": "DPM++ 2M Karras",
        "cfg_scale": 8,
        "width": width,
        "height": height,
        "batch_size": 1,
        "restore_faces": False,
        "save_images": False,
        "send_images": True,
        "override_settings": {
            "sd_model_checkpoint": MODEL
        }
    }

    print("🎨 Generating image...")
    try:
        response = requests.post(SD_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        # Decode image (base64 → bytes)
        image_base64 = data["images"][0]
        image_bytes = base64.b64decode(image_base64)

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Add timestamp to filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_path.rstrip('.png')}_{timestamp}.png"

        # Save to disk
        with open(filename, "wb") as f:
            f.write(image_bytes)

        print(f"✅ Image generated: {filename}")
        return filename

    except requests.RequestException as e:
        print("❌ Error generating image:", e)
        return None
