from modules.rss_reader import get_latest_titles
from modules.prompt_generator import generate_prompt
from modules.image_generator import generate_image
from datetime import datetime
# from modules.instagram import post_image
from config import IMAGE_DIR
import os

def main():
    # --- 1️⃣ Read news ---
    titles = get_latest_titles()
    if not titles:
        print("⚠️ No news found in the RSS feed.")
        return

    print("📰 News found:")
    for t in titles:
        print("-", t)

    # --- 2️⃣ Generate artistic prompt ---
    prompt = generate_prompt(titles)
    print("\n🎭 Generated prompt:")
    print(prompt)

    # --- 3️⃣ Generate image ---
    output_dir = IMAGE_DIR
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"news_art_{datetime.now().strftime('%Y%m%d')}.png")

    image_path = generate_image(prompt, filename)

    if image_path:
        print(f"\n✅ Daily image ready: {image_path}")
    else:
        print("❌ Error generating image.")

if __name__ == "__main__":
    main()
