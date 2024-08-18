from newspaper import Article
from bs4 import BeautifulSoup
import json

def get_article_data_nyt(url):
    article = Article(url)
    article.download()
    article.parse()
    soup = BeautifulSoup(article.html, 'html.parser')
    
    main_image = article.top_image  # Try to get the image using 'newspaper'
    
    if not main_image:  # Fallback mechanism
        main_content = soup.find('main', {'role': 'main'})  # Adjust based on website structure
        if main_content:
            img_tag = main_content.find('img')
            if img_tag and 'src' in img_tag.attrs:
                main_image = img_tag['src']

    # Get headline
    headline_tag = soup.find('h1')
    headline = headline_tag.text.strip() if headline_tag else None

    # Get byline
    byline_tag = soup.find('span', itemprop='name')
    byline = byline_tag.text.strip() if byline_tag else None

    # Get image captions
    caption_tags = soup.find_all('figcaption')
    captions = [tag.text.strip() for tag in caption_tags]
    
    # Get article text
    article_container = soup.find('section', {'name': 'articleBody'})
    if article_container:
        paragraph_tags = article_container.find_all('p')
        article_text = ' '.join([p.text for p in paragraph_tags])
    else:
        article_text = None

    # Get publication date
    date_tag = soup.find('time')
    publication_date = date_tag['datetime'] if date_tag and date_tag.has_attr('datetime') else None
    
    return {
        "url": url,
        "headline": headline,
        "byline": byline,
        "main_image": main_image,  # Added main_image
        "image_captions": captions,
        "article": article_text,
        "publication_date": publication_date
    }
