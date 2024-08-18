from collections import deque
import logging
from datetime import datetime
import os

# Initialize logging
def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    today = datetime.now().strftime("%Y-%m-%d")
    log_filename = f'logs/log_{today}.txt'
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

setup_logging()  # Initialize logging

RETRY_LIMIT = 3

retry_queues = {}  # A dictionary of retry queues, one per source

def enqueue_failed_article(source_name, entry):
    if source_name not in retry_queues:
        retry_queues[source_name] = deque()
    retry_count = entry.get('retry_count', 0) + 1
    entry['retry_count'] = retry_count
    retry_queues[source_name].append(entry)
    logging.info(f"Enqueued article for retry from {source_name}. Retry count: {retry_count}. Queue length is now {len(retry_queues[source_name])}.")

def dequeue_retry_article(source_name):
    retry_article = retry_queues.get(source_name).popleft() if retry_queues.get(source_name) else None
    if retry_article:
        logging.info(f"Dequeued article for retry from {source_name}. Queue length is now {len(retry_queues[source_name])}.")
    return retry_article

def has_retries(source_name):
    has_retry = bool(retry_queues.get(source_name))
    if has_retry:
        logging.info(f"Retry queue for {source_name} is not empty.")
    return has_retry
