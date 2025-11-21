import os
import requests
from modules.utils import get_s3_client, generate_unique_filename # Using utilities for R2 setup

# --- CLOUDFLARE WORKERS AI CONFIGURATION ---

# Credentials (Read from environment variables loaded in main.py)
CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
CF_API_TOKEN = os.getenv("CF_API_TOKEN")
CF_MODEL_ID = os.getenv("CF_MODEL_ID", "@cf/stabilityai/stable-diffusion-xl-base-1.0")

# Default parameters for SDXL generation
DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 1024
DEFAULT_NEGATIVE_PROMPT = """
    low quality, blurry, ugly, watermark, distortion, noise, out of focus, 
    extra limbs, bad anatomy, deformed, pixelated, error, text, signature
""".strip()
DEFAULT_STEPS = 30 
DEFAULT_GUIDANCE_SCALE = 7.5

# Construct the base URL for the Cloudflare AI API
CF_API_URL = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/{CF_MODEL_ID}"

# --- R2 CONFIGURATION ---
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
R2_PUBLIC_URL_BASE = os.getenv("R2_PUBLIC_URL_BASE")

# Default generation parameters (kept for function signature)
DEFAULT_WIDTH = 832
DEFAULT_HEIGHT = 1040 # 4:5 vertical for Instagram

# ... (DEFAULT_NEGATIVE_PROMPT, DEFAULT_STEPS, DEFAULT_GUIDANCE_SCALE remain the same) ...


def upload_to_r2(key, image_bytes):
    """Uploads the image bytes directly to Cloudflare R2."""
    s3_client = get_s3_client()
    if not s3_client:
        return None

    try:
        s3_client.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=key,
            Body=image_bytes,
            ContentType='image/png'
        )
        # R2 files are publicly accessible via the R2_PUBLIC_URL_BASE
        public_url = f"{R2_PUBLIC_URL_BASE}/{key}"
        print(f"✅ Image uploaded to R2: {public_url}")
        return public_url
    except Exception as e:
        print(f"❌ Error uploading image to R2: {e}")
        return None


def generate_image_workers_ai(prompt, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
    """
    Generates an image via Cloudflare Workers AI and uploads it to R2.
    Returns the public R2 URL.
    """
    if not CF_ACCOUNT_ID or not CF_API_TOKEN:
        print("❌ Error: CF credentials not set.")
        return None

    # ... (payload and headers logic remains the same) ...
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

        # 1. Generate unique key for R2
        r2_key = generate_unique_filename(extension=".png")

        # 2. Upload image bytes to R2
        public_url = upload_to_r2(r2_key, image_bytes)
        
        return public_url

    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP Error during image generation: {e}")
        try:
            # Try printing the API response content for debugging (it might be a JSON error message)
            print("API Response (text):", response.text)
        except Exception:
            print("❌ Error printing API response text.")
            pass
        return None
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return None