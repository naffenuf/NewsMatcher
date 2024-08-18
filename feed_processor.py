import os
import itertools
import json
import feedparser
import logging
from datetime import datetime
from urllib.parse import urlparse
from utilities import sanitize_url, remove_boilerplate
from scrapers.nyt_scraper import get_article_data_nyt
from scrapers.post_scraper import get_article_data_post
from scrapers.dailynews_scraper import get_article_data_dailynews
from scrapers.generic_scraper import get_article_data_generic 
from scrapers.daily_mail_scraper import get_daily_mail_article_data
from scrapers.ny_sun_scraper import get_nysun_article_data
from retry_handler import enqueue_failed_article, dequeue_retry_article, has_retries

def process_feeds(rss_feed_data):
    MAX_FILENAME_LENGTH = 250
    
    article_counts = {}
    articles = {}
    source_attributes = {}
    today = datetime.now().strftime("%Y-%m-%d")
    
    if not os.path.exists(today):
        os.makedirs(today)

    for feed_data in rss_feed_data:
        feed = feed_data['rss_feed']
        keyword = feed_data['keyword']
        source_name = urlparse(feed).netloc.replace('.', '_')
        full_path = os.path.join(today, source_name)
        all_entries = feedparser.parse(feed).entries
        filtered_entries = [entry for entry in all_entries if keyword in entry.link]
        articles[source_name] = filtered_entries
        article_counts[source_name] = 0
        os.makedirs(full_path, exist_ok=True)
        
        source_attributes[source_name] = {
            'pub_name': feed_data['pub_name'],
            'bias': feed_data['bias'],
            'nickname': feed_data['nickname'],
            'article_type': feed_data['article_type'],
            'boilerplate': feed_data.get('boilerplate', []) 
        }

    entry = None
    source_cycle = itertools.cycle(articles.keys())

    while True:
        all_processed = all(article_counts[source_name] >= len(articles[source_name]) for source_name in articles.keys())
        if all_processed:
            logging.info("All articles processed. Exiting.")
            break

        try:
            source_name = next(source_cycle)
            pub_name = source_attributes[source_name]['pub_name']
            bias = source_attributes[source_name]['bias']
            nickname = source_attributes[source_name]['nickname']
            article_type = source_attributes[source_name]['article_type']
            
            if has_retries(source_name):
                entry = dequeue_retry_article(source_name)
            else:
                if article_counts[source_name] >= len(articles[source_name]):
                    continue
                entry = articles[source_name][article_counts[source_name]]
                article_counts[source_name] += 1

            sanitized_url = sanitize_url(entry.link)
            
            # Truncate the filename if it's too long
            truncated_url = sanitized_url[:MAX_FILENAME_LENGTH - len(today) - len(source_name) - 6]
            file_path = os.path.join(today, source_name, f"{truncated_url}.json")

            if os.path.exists(file_path):
                logging.info(f'Skipping already downloaded article from {source_name}, URL: {entry.link}')
                continue

            if 'nytimes' in source_name:
                article_data = get_article_data_nyt(entry.link)
            elif 'nypost' in source_name:
                article_data = get_article_data_post(entry.link)
            elif 'nydailynews' in source_name:
                article_data = get_article_data_dailynews(entry.link)
            # elif 'dailymail' in source_name:
            #     article_data = get_daily_mail_article_data(entry.link)
            elif 'nysun' in source_name:
                article_data = get_nysun_article_data(entry.link)
            else:
                article_data = get_article_data_generic(entry.link)

            if article_data is not None:
                article_data['pub_name'] = pub_name
                article_data['bias'] = bias
                article_data['nickname'] = nickname
                article_data['article_type'] = article_type
                article_data['boilerplate'] = source_attributes[source_name].get('boilerplate', []) 
                article_data = remove_boilerplate(article_data)

                with open(file_path, 'w') as file:
                    json.dump(article_data, file)
                logging.info(f'Successfully processed article from {source_name}, URL: {entry.link}')
            else:
                logging.info(f'Skipping article due to NoneType, URL: {entry.link}')

        except Exception as e:
            logging.error(f'Error processing article: {str(e)}, URL: {entry.link if entry else "Unknown"}')
            enqueue_failed_article(source_name, entry)
