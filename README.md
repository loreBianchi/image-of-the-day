# Image Of The Day: Daily AI-Generated Art from News Feeds

## Introduction
**Image Of The Day** is a serverless Python project designed to automate the creation of artistic content based on real-time news headlines. The system integrates RSS feed reading, creative prompt generation using Google Gemini, and high-quality image synthesis using Stable Diffusion XL via Cloudflare Workers AI.

Generated images and associated metadata (prompt, source news) are stored securely in a Cloudflare R2 bucket and served to users via a lightweight FastAPI gallery application hosted on Fly.io.

## Project Architecture
The project is structured into two separate, containerized components for robust operation:
1. Daily Job (main.py): The scheduled script that executes the content generation pipeline.
2. Gallery API (app/api.py): The web server that fetches metadata from R2 and serves the frontend gallery.
3. The entire workflow is designed to be serverless and cost-effective, leveraging the free tiers of multiple cloud providers.