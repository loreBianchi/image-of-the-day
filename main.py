import os
from dotenv import load_dotenv
import sys

from modules.rss_reader import get_latest_titles
from modules.prompt_generator import generate_prompt
from modules.image_generator import generate_image_workers_ai
from modules.utils import generate_unique_filename
from config import IMAGE_DIR # Assumes IMAGE_DIR is defined in config.py (e.g., "app/static/images")
# from modules.instagram import post_image 

# Load environment variables IMMEDIATELY for all modules
load_dotenv() 

def main():
    print("🚀 Starting AI News Artist Daily Job...")
    
    # --- Pre-Requisites Check ---
    # Check for the key required for prompt generation
    if 'GEMINI_API_KEY' not in os.environ:
        print("\n⚠️ WARNING: GEMINI_API_KEY environment variable is not set. Cannot generate prompt.")
        sys.exit(1) # Exit if the core dependency is missing

    # --- 1️⃣ Read News ---
    # Assumes a default RSS feed URL is configured internally in rss_reader.py
    titles = get_latest_titles() 
    if not titles:
        print("⚠️ No news found in the RSS feed.")
        return

    print(f"📰 Found {len(titles)} headlines.")

    # --- 2️⃣ Generate Artistic Prompt ---
    prompt = generate_prompt(titles)

    if prompt:
        print("\n🎭 Generated prompt:")
        print("-" * 50)
        print(prompt)
        print("-" * 50)
    else:
        print("\n❌ Failed to generate the prompt.")
        return
    
    # --- 3️⃣ Generate Image ---
    output_base_dir = IMAGE_DIR
    
    # Generate the unique full path using the utility function
    image_path_to_save = generate_unique_filename(
        base_dir=output_base_dir, 
        base_name="news_art",
        extension=".png"
    )

    # Use default 4:5 vertical size for optimal Instagram viewing
    image_path = generate_image_workers_ai(
        prompt=prompt, 
        output_path=image_path_to_save,
        width=832,
        height=1040 # 4:5 ratio
    )
    
    if image_path:
        print(f"\n✅ Daily image saved: {image_path}")
        
        # --- 4️⃣ Publish (Optional) ---
        # post_image(image_path, prompt) 
        # print("✅ Image posted to Instagram.")

    else:
        print("❌ Error generating image.")        


if __name__ == "__main__":
    main()