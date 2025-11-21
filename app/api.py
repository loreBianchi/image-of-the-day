from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables (essential if any template or setup relies on them)
load_dotenv() 

app = FastAPI(title="AI News Artist Gallery")

# Define the directory where images are saved (relative to project root)
IMAGE_DIR = "app/static/images"
os.makedirs(IMAGE_DIR, exist_ok=True) 

# Mount static files: /static URL maps to app/static directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def read_root():
    return {"message": "Welcome to the AI News Artist Gallery. View generated images at /gallery."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/gallery")
def show_gallery(request: Request):
    """
    Renders the gallery page by listing all PNG files and reading associated TXT prompts.
    """
    images = []

    try:
        # List and sort files to show the newest first
        files = sorted(os.listdir(IMAGE_DIR), reverse=True)
    except FileNotFoundError:
        return templates.TemplateResponse("gallery.html", {"request": request, "images": []})


    for file in files:
        if file.endswith(".png"):
            # Attempt to extract date/time from the standardized filename format (news_art_YYYYMMDD_HHMMSS.png)
            date = "Unknown Date"
            prompt_text = "Prompt not found."
            
            try:
                parts = file.split('_')
                if len(parts) >= 3:
                    date_str = parts[-2]
                    time_str = parts[-1].split('.')[0]
                    date_time = datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")
                    date = date_time.strftime("%d/%m/%Y %H:%M")
            except Exception:
                print("❌ Error parsing date from filename:", file)
                # If parsing fails, use a default
                pass

            # Construct the path for the prompt file (.txt)
            prompt_file = file.replace(".png", ".txt")
            prompt_path = os.path.join(IMAGE_DIR, prompt_file)
            
            if os.path.exists(prompt_path):
                with open(prompt_path, "r", encoding="utf-8") as f:
                    prompt_text = f.read().strip()
            
            images.append({
                # The URL path must point to the static file endpoint
                "url": f"/static/images/{file}",
                "prompt": json.dumps(prompt_text),
                "date": date
            })

    return templates.TemplateResponse("gallery.html", {"request": request, "images": images})