import json  # Import json for reading the JSON file
from log_handler import setup_logging
from feed_processor import process_feeds

if __name__ == '__main__':
    with open('rss_feeds.json', 'r') as f:
        rss_feed_data = json.load(f)
    
    setup_logging()
    process_feeds(rss_feed_data)

