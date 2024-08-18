import os
import subprocess
import logging
import time
from datetime import datetime

# Initialize logging
def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    today = datetime.now().strftime("%Y-%m-%d")
    log_filename = f'logs/log_{today}.txt'
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    setup_logging()  # Initialize logging
    start_time_total = time.time()  # Capture the total start time

    try:
        # Run delete-matches.py
        logging.info("Starting delete-matches.py...")
        print("Starting delete-matches.py...")
        subprocess.run(["python3", "delete-matches.py"])
        logging.info("Completed delete-matches.py")
        print("Completed delete-matches.py")

        # Run getarticles.py
        logging.info("Starting getarticles.py...")
        print("Starting getarticles.py...")
        subprocess.run(["python3", "getarticles.py"])
        logging.info("Completed getarticles.py")
        print("Completed getarticles.py")

        # Run strip_unicode.py
        logging.info("Starting unicodestripper.py...")
        print("Starting unicodestripper.py...")
        subprocess.run(["python3", "unicodestripper.py"])
        logging.info("Completed unicodestripper.py")
        print("Completed unicodestripper.py")

        # Run createindex.py
        logging.info("Starting createindex.py...")
        print("Starting createindex.py...")
        subprocess.run(["python3", "createindex.py"])
        logging.info("Completed createindex.py")
        print("Completed createindex.py")

        # Run find_matching_articles.py
        logging.info("Starting find_matching_articles.py...")
        print("Starting find_matching_articles.py...")
        subprocess.run(["python3", "find_matching_articles.py"])
        logging.info("Completed find_matching_articles.py")
        print("Completed find_matching_articles.py")

        # Run deduplicate_matches.py
        logging.info("Starting deduplicate_matches.py...")
        print("Starting deduplicate_matches.py...")
        subprocess.run(["python3", "deduplicate_matches.py"])
        logging.info("Completed deduplicate_matches.py")
        print("Completed deduplicate_matches.py")

        # Run check-accuracy.py
        logging.info("Starting check-accuracy.py...")
        print("Starting check-accuracy.py...")
        subprocess.run(["python3", "check-accuracy.py"])
        logging.info("Completed check-accuracy.py")
        print("Completed check-accuracy.py")

        # Run send-data.py
        logging.info("Starting send-data.py...")
        print("Starting send-data.py...")
        subprocess.run(["python3", "send-data.py"])
        logging.info("Completed hsend-data.py")
        print("Completed send-data.py")

        end_time_total = time.time()  # Capture the total end time
        elapsed_time_total = end_time_total - start_time_total  # Calculate total elapsed time
        print(f"Total elapsed time: {elapsed_time_total:.2f} seconds")  # Print total elapsed time to the terminal

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")
