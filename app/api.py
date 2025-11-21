from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from datetime import datetime
import json
from dotenv import load_dotenv
from modules.utils import load_gallery_metadata # Import the new R2 metadata loader

# Load environment variables (needed for R2 client config in utils)
load_dotenv() 

app = FastAPI(title="AI News Artist Gallery")

# Define the directory for static assets (e.g., CSS/JS, not images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Note: The /images directory is no longer needed as images are served from R2

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def show_gallery(request: Request):
    """
    Frontend route. Fetches the gallery metadata from R2 and displays the images.
    """
    
    # Load the list of image metadata (ordered by recency in the JSON file)
    images_data = load_gallery_metadata()

    # Prepare data for template rendering
    images = []
    for entry in images_data:
        images.append({
            "url": entry.get("image_url"),
            "prompt": json.dumps(entry.get("prompt", "No prompt available")),
            "date": datetime.fromisoformat(entry["timestamp"]).strftime("%d/%m/%Y %H:%M"),
            # Include news titles for display/debugging
            "news_titles": entry.get("news_titles", []) 
        })

    return templates.TemplateResponse("gallery.html", {"request": request, "images": images})