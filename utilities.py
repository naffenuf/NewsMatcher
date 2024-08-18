import re
from urllib.parse import urlparse
import logging


def sanitize_url(url):
    parsed = urlparse(url)
    path = parsed.path if parsed.path != '/' else ''
    sanitized = f"{parsed.netloc}{path}".replace('.', '_').replace('/', '_').replace('-', '_').replace(':', '_')
    return sanitized

def remove_boilerplate(article_data):
    article = article_data.get('article', '')
    boilerplates = article_data.get('boilerplate', [])
    logging.info(f"Initial article length: {len(article)}")
    logging.info(f"Boilerplates to remove: {boilerplates}")

    for bp in boilerplates:
        article = article.replace(bp, '')
    logging.info(f"Final article length: {len(article)}")

    article_data['article'] = article
    return article_data

