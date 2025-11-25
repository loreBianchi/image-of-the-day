import os
import sys
from dotenv import load_dotenv
from datetime import datetime

from modules.rss_reader import get_latest_titles
from modules.prompt_generator import generate_prompt
from modules.image_generator import generate_image_workers_ai
from modules.utils import save_gallery_metadata

# Load environment variables IMMEDIATELY for all modules
load_dotenv() 


def main():
    """
    Main function to run the daily AI Image of the Day job.
    1. Reads latest news titles from RSS feed.
    2. Generates an artistic prompt using Gemini API.
    3. Generates an image via Cloudflare Workers AI and uploads it to R2.
    4. Saves metadata to R2.
    5. (Optional) Publishes the image on Instagram.
    """
    print("🚀 Starting AI News Artist Daily Job...")
    
    # --- Pre-Requisites Check ---
    if 'GEMINI_API_KEY' not in os.environ:
        print("\n🚧 WARNING: GEMINI_API_KEY environment variable is not set. Cannot generate prompt.")
        sys.exit(1)

    # --- 1️⃣ Read News ---
    titles = get_latest_titles() 
    if not titles:
        print("⚠️ No news found in the RSS feed.")
        return

    print(f"📰 Found {len(titles)} headlines.")

    # --- 2️⃣ Generate Artistic Prompt ---
    prompt = generate_prompt(titles)

    if not prompt:
        print("\n❌ Failed to generate the prompt.")
        return
    
    print("\n🎭 Generated prompt:")
    print("-" * 50)
    print(prompt)
    print("-" * 50)

    # --- 3️⃣ Generate and Upload Image to R2 (4:5 vertical) ---
    image_url = generate_image_workers_ai(
        prompt=prompt,
        width=832,
        height=1040 
    )
    
    if not image_url:
        print("❌ Error generating or uploading image to R2.")        
        return

    print(f"\n✅ Daily image ready and uploaded: {image_url}")

    # --- 4️⃣ Save Metadata to R2 ---
    metadata_entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "news_titles": titles,
        "image_url": image_url
    }
    
    if save_gallery_metadata(metadata_entry):
        print("✅ Metadata successfully updated on R2.")
    else:
        print("❌ Failed to save metadata on R2.")

    # --- 5️⃣ Publish (Optional) ---
    # post_image(image_url, prompt) 


if __name__ == "__main__":
    main()