import requests
import json
import logging
import re

def remove_html_tags(text):
    return re.sub('<[^<]+?>', '', text)

def extract_values(obj, key):
    arr = []

    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(remove_html_tags(v).replace('\xa0', ' ').replace('\u00b4', "'"))
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

def get_daily_mail_article_data(url):
    try:
        match = re.search(r'article-(\d+)', url)
        if match:
            article_num = match.group(1)
        else:
            print(f"Could not extract article number from URL: {url}")
            return None

        api_url = f'http://api.dailymail.co.uk/mobile/2.0/article/{article_num}'
        response = requests.get(api_url)
        
        if response.status_code == 200:
            article_data = json.loads(response.text)
            
            headline_values = extract_values(article_data, 'headline')
            byline_values = extract_values(article_data, 'byline')
            date_values = extract_values(article_data, 'publicationDate')
            content_values = extract_values(article_data, 'content')

            article_content = ' '.join(content_values)
            if ' ' not in article_content[:30]:
                logging.info(f'Skipping article {article_num} due to unwanted beginning sequence.')
                return None

            
            # Select the largest image by dimension
            images = article_data.get('images', [])
            if images:
                largest_image = max(images, key=lambda x: x.get('width', 0) * x.get('height', 0))
                main_image_url = largest_image.get('hostUrl')
            else:
                main_image_url = None
            
            return {
                "url": url,
                "headline": headline_values[0] if headline_values else '',
                "byline": byline_values[0] if byline_values else '',
                "main_image": main_image_url,  # Added main_image
                "image_captions": [],  # Replace with actual extraction logic
                "article": article_content,
                "publication_date": date_values[0] if date_values else ''
            }
        else:
            logging.error(f'Request failed with status code {response.status_code} for article {article_num}')
            return None

    except Exception as e:
        logging.error(f'Error occurred while processing article {article_num}: {e}')
        return None
