import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- RSS FEED CONFIGURATION ---
RSS_FEED = "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"

# --- CLOUDFLARE WORKERS AI CONFIGURATION ---
CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
CF_API_TOKEN = os.getenv("CF_API_TOKEN")
CF_MODEL_ID = os.getenv("CF_MODEL_ID", "@cf/stabilityai/stable-diffusion-xl-base-1.0")

# Default generation parameters
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
R2_PUBLIC_URL_BASE = os.getenv("R2_PUBLIC_URL_BASE")
R2_ENDPOINT_URL = os.getenv("R2_ENDPOINT_URL")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")

GALLERY_METADATA_KEY = "gallery_data.json" # Central file for all metadata


# Default generation parameters (kept for function signature)
DEFAULT_WIDTH = 832
DEFAULT_HEIGHT = 1040 # 4:5 vertical for Instagram

# Instagram
IG_USERNAME = "tuo_username"
IG_PASSWORD = "tua_password"
