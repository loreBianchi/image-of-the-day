# Image Of The Day: Daily AI-Generated Art from News Feeds

## Introduction
**Image Of The Day** s a serverless project that automatically creates a daily piece of AI-generated artwork inspired by real-time news.
A scheduled Python job processes RSS feeds, generates an artistic prompt using Google Gemini, and produces a high-quality image (e.g., via Stable Diffusion XL using Cloudflare Workers AI).
All generated assets — images and metadata — are stored in a Cloudflare R2 bucket and displayed in a React-based gallery served through Cloudflare Pages.

## Project Architecture
The system is composed of three independent parts that work asynchronously and communicate exclusively through Cloudflare R2.

### Daily Job (Python Cron)

A lightweight Python script (main.py) runs once per day via GitHub Actions or Cloudflare Pages Cron. It performs three tasks:
   - RSS Parsing: Reads news headlines from selected sources (feedparser).
   - Prompt Generation: Uses Google Gemini to combine and summarize news into an artistic prompt.
   - Image Generation & Upload: enerates the artwork through an AI API (e.g., Cloudflare Workers AI), then uploads the image and metadata (gallery_data.json) to R2 using boto3.

### Cloudflare R2 (Storage Layer)

R2 serves as the single source of truth for the entire application.
   - Images: Stores the generated .png files.
   - Metadata: Stores the JSON file (gallery_data.json) containing the prompts, sources, and image URLs, sorted by date.

### Frontend (React TS)
A lightweight React application displays the full gallery and the daily image.
- Live app: [https://image-of-the-day-fe.pages.dev/](https://image-of-the-day-fe.pages.dev/) 
- Frontend repository: [frontend repository](https://github.com/loreBianchi/image-of-the-day-fe) 
