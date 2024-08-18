from newspaper import Article
from bs4 import BeautifulSoup
import json
import logging

# Function to scrape individual articles
def get_nysun_article_data(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        html_content = article.html
        soup = BeautifulSoup(html_content, 'html.parser')
        
        main_image = article.top_image  # Try to get the image using 'newspaper'
        
        if not main_image:  # Fallback mechanism
            main_content = soup.find('div', {'class': 'main-content'})
            if main_content:
                img_tag = main_content.find('img')
                if img_tag and 'src' in img_tag.attrs:
                    main_image = img_tag['src']
        
        h1_tags = soup.find_all('h1')
        headline = h1_tags[1].text if len(h1_tags) > 1 else None

        byline_tag = soup.find('div', {'class': 'author-byline'})
        byline = byline_tag.text.strip().replace('\\n', ' ').replace('  ', ' ') if byline_tag else article.authors[0] if article.authors else None

        publication_date_tag = soup.find('time')
        publication_date = publication_date_tag.text.strip() if publication_date_tag else article.publish_date.strftime("%Y-%m-%d") if article.publish_date else None

        caption_tags = soup.find_all('figcaption')
        captions = [tag.text.strip() for tag in caption_tags]

        paragraph_tags = soup.find_all('p', class_=lambda x: x != 'copyright')
        article_text = ' '.join([p.text for p in paragraph_tags]).strip()
        
        return {
            "url": url,
            "headline": headline,
            "byline": byline,
            "main_image": main_image,
            "image_captions": captions,
            "article": article_text,
            "publication_date": publication_date
        }

    except Exception as e:
        logging.error(f"Error scraping article: {str(e)}, URL: {url}")
        return None

# Function to fetch multiple articles and store them in a JSON file
def fetch_and_store_articles(article_urls):
    all_articles = []
    
    for url in article_urls:
        article_data = get_article_data_generic(url)
        
        if article_data is not None:
            all_articles.append(article_data)

    with open('articles.json', 'w') as f:
        json.dump(all_articles, f)

# Example usage
if __name__ == '__main__':
    article_urls = [
        'https://example.com/article1',
        'https://example.com/article2',
        # Add more article URLs here
    ]

    fetch_and_store_articles(article_urls)
