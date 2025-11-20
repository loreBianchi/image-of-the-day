from modules.rss_reader import get_latest_titles
from modules.prompt_generator import generate_prompt_gemini
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

    if 'GEMINI_API_KEY' not in os.environ:
        print("\n⚠️ ATTENZIONE: La variabile d'ambiente GEMINI_API_KEY non è impostata. Lo script non può eseguire la chiamata API.")
        print("Per usarlo, ottieni una chiave API e impostala prima di eseguire lo script.")
    else:
         # --- 2️⃣ Generate artistic prompt ---
        prompt = generate_prompt_gemini(titles)

        if prompt:
            print("\n🎭 Generated prompt:")
            print("-" * 50)
            print(prompt)
            print("-" * 50)
        else:
            print("\n❌ La generazione del prompt non è riuscita.")

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
    