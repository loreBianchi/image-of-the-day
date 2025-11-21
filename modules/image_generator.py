import os
import requests
from modules.utils import get_text_filepath

# --- CLOUDFLARE WORKERS AI CONFIGURATION ---

# Credentials from environment variables (readed in main.py)
CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
CF_API_TOKEN = os.getenv("CF_API_TOKEN")
CF_MODEL_ID = os.getenv("CF_MODEL_ID", "@cf/stabilityai/stable-diffusion-xl-base-1.0")

# Default parameters for SDXL (kept here for isolation)
DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 1024
DEFAULT_NEGATIVE_PROMPT = """
    low quality, blurry, ugly, watermark, distortion, noise, out of focus, 
    extra limbs, bad anatomy, deformed, pixelated, error, text, signature
""".strip()
DEFAULT_STEPS = 30 
DEFAULT_GUIDANCE_SCALE = 7.5

# Constructs the base URL for the Cloudflare API
CF_API_URL = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/{CF_MODEL_ID}"


def generate_image_workers_ai(prompt, output_path, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
    """
    Generates an image using the Cloudflare Workers AI API (Stable Diffusion XL).
    The output_path parameter is the full and final path of the PNG file.
    """
    if not CF_ACCOUNT_ID or not CF_API_TOKEN:
        print("❌ Error: CF_ACCOUNT_ID or CF_API_TOKEN variables not set.")
        return None

    payload = {
        "prompt": prompt,
        "negative_prompt": DEFAULT_NEGATIVE_PROMPT,
        "width": width,
        "height": height,
        "steps": DEFAULT_STEPS,
        "guidance_scale": DEFAULT_GUIDANCE_SCALE,
    }

    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    print(f"🎨 Generating image with Cloudflare Workers AI ({CF_MODEL_ID})...")
    try:
        response = requests.post(CF_API_URL, headers=headers, json=payload)
        response.raise_for_status()

        # Cloudflare returns the image directly in bytes
        image_bytes = response.content

        # The directory has already been created by generate_unique_filename in utils
        
        # Save the image to disk
        with open(output_path, "wb") as f:
            f.write(image_bytes)

        # Save the prompt in the associated text file
        text_filepath = get_text_filepath(output_path)
        with open(text_filepath, "w", encoding="utf-8") as f:
            f.write(prompt)

        print(f"✅ Image generated: {output_path}")
        return output_path

    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP error during image generation: {e}")
        try:
            print("API response (text):", response.text)
        except Exception:
            pass
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None