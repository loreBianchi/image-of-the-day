import feedparser
from config import RSS_FEED

def get_latest_titles():
    feed = feedparser.parse(RSS_FEED)
    # print("Feed RSS analizzato.")
    # print("Numero di voci nel feed:", len(feed.entries))
    # print("Voci trovate:", [entry.title for entry in feed.entries])
    if not feed.entries:
        return None
    titles_list = [entry.title for entry in feed.entries]
    titles = "\n - ".join(titles_list)
    return titles
