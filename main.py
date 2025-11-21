from modules.rss_reader import get_latest_titles
from modules.prompt_generator import generate_prompt
from modules.image_generator import generate_image_workers_ai
from modules.utils import generate_unique_filename # <--- Importato da utils
# from modules.instagram import post_image
from config import IMAGE_DIR
import os
import sys

def main():
    print("🚀 Starting AI News Artist...")
    
    # Check crucial environment variables
    if 'GEMINI_API_KEY' not in os.environ:
        print("\n⚠️ WARNING: The GEMINI_API_KEY environment variable is not set. The script cannot make the API call.")
        print("To use it, obtain an API key and set it before running the script.")
        # We do not exit here because prompt generation does not occur, but execution continues if necessary.
    
    # --- 1️⃣ Read news ---
    titles = get_latest_titles()
    if not titles:
        print("⚠️ No news found in the RSS feed.")
        return

    print("📰 News found:")
    for t in titles:
        print("-", t)

    # --- 2️⃣ Generate artistic prompt ---
    prompt = generate_prompt(titles) # The function will internally handle the missing GEMINI_API_KEY case

    if prompt:
        print("\n🎭 Generated prompt:")
        print("-" * 50)
        print(prompt)
        print("-" * 50)
    else:
        print("\n❌ Prompt generation failed.")
        return
    
    # --- 3️⃣ Generate image ---
    output_dir = IMAGE_DIR
    
    # Generate the file path using the centralized function in utils
    image_path_to_save = generate_unique_filename(
        base_dir=output_dir, 
        base_name="news_art",
        extension=".png"
    )

    image_path = generate_image_workers_ai(prompt=prompt, output_path=image_path_to_save)
    
    if image_path:
        print(f"\n✅ Daily image ready: {image_path}")
    else:
        print("❌ Error generating image.")        


if __name__ == "__main__":
    main()