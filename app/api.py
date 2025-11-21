from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel
from datetime import datetime
import json
import os

app = FastAPI(title="AI News Artist API")

# Servire immagini statiche
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# --- Modello per la request ---
class GenerateImageRequest(BaseModel):
    feed_url: str = None        # se vuoi leggere da feed
    prompt: str = None          # o prompt custom
    width: int = 1024
    height: int = 1024

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI News Artist API. Use the /generate endpoint to create images."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/gallery")
def show_gallery(request: Request):
    image_dir = "app/static/images"
    images = []

    for file in sorted(os.listdir(image_dir), reverse=True):
        if file.endswith(".png"):
            # Supponiamo che il nome del file contenga il modello, es: news_art_DreamShaper_20231102.png
            parts = file.split('_')
            date = datetime.strptime(parts[2], "%Y%m%d").date() if len(parts) > 2 else "Unknown"
            prompt_file = file.replace(".png", ".txt")
            prompt_path = os.path.join(image_dir, prompt_file)
            prompt_text = ""
            if os.path.exists(prompt_path):
                with open(prompt_path, "r") as f:
                    prompt_text = f.read()
            images.append({
                "url": f"/static/images/{file}",
                "prompt": json.dumps(prompt_text.strip()),
                "date": date
            })

    return templates.TemplateResponse("gallery.html", {"request": request, "images": images})