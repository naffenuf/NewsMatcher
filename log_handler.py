import logging
from datetime import datetime

def setup_logging():
    today = datetime.now().strftime("%Y-%m-%d")
    log_filename = f'logs/log_{today}.txt'
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
