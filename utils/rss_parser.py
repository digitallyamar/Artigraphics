import feedparser

def parse_rss_feed(rss_url):
    feed = feedparser.parse(rss_url)
    articles = []
    for entry in feed.entries:
        articles.append({
            'title': entry.get('title', ''),
            'link': entry.get('link', ''),
            'description': entry.get('description', '')
        })
    return articles