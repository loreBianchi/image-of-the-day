from modules.rss_reader import get_latest_titles
from modules.prompt_generator import generate_prompt
from modules.image_generator import generate_image
# from modules.instagram import post_image
from config import IMAGE_DIR
import os
import time

def run():
    print("Process started ... 🚀")
    titles = get_latest_titles()
    print("Titles 📰:\n - ", titles)
    if not titles:
        print("No titles found in the RSS feed.")
        return

    prompt = generate_prompt(titles)
    print("Prompt:", prompt)

    timestamp = int(time.time())
    filename = os.path.join(IMAGE_DIR, f"{titles[:20].replace(' ', '_')}{timestamp}.png")
    generate_image(prompt, filename)
    print("Image generated:", filename)

    # If you want to post on Instagram
    # post_image(filename, caption=titles)

if __name__ == "__main__":
    run()
