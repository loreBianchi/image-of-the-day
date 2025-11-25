# Image Of The Day: Daily AI-Generated Art from News Feeds

## Introduction
**Image Of The Day** is a serverless project designed to automate the creation of unique artistic content based on real-time news.
The system runs a Python Cron Job that reads RSS feeds, generates creative prompts using Google Gemini, and produces a high-qualiy image (e.g., via Stable Diffusion XL using Cloudflare Workers AI).
The generated content (images and JSON metadata) is stored in a Cloudflare R2 bucket and served to users through a React gallery managed by a Cloudflare Worker.

## Project Architecture
The architecture is now divided into three key components that work asynchronously, communicating exclusively via Cloudflare R2:

### Daily Job (Python Cron)

This is a simple Python script (main.py) that runs once daily (typically via GitHub Actions or Cloudflare Pages Cron):
   - RSS Parsing: Reads news headlines from selected sources (feedparser).
   - Prompt Generation: Uses Google Gemini to combine and summarize news into an artistic prompt.
   - Image Generation & Upload: Calls the AI API (e.g., Workers AI) to generate the image and uploads the result, along with the updated metadata (gallery_data.json), to the R2 bucket (boto3).

### Cloudflare R2 (Storage Layer)

R2 serves as the single source of truth for the entire application.
   - Images: Stores the generated .jpg files.
   - Metadata: Stores the JSON file (gallery_data.json) containing the prompts, sources, and image URLs, sorted by date.

### Frontend (React TS)

TODO
