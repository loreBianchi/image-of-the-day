import feedparser
import random
from config import RSS_FEED

def get_latest_titles():
    feed = feedparser.parse(RSS_FEED)
    if not feed.entries:
        return None
    all_titles = [entry.title for entry in feed.entries]
    titles = random.sample(all_titles, min(5, len(all_titles)))
    return titles
