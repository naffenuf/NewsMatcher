from newspaper import Article
from bs4 import BeautifulSoup
import json

def get_article_data_dailynews(url):
    article = Article(url)
    article.download()
    article.parse()
    soup = BeautifulSoup(article.html, 'html.parser')
    
    main_image = article.top_image  # Try to get the image using 'newspaper'
    
    if not main_image:  # Fallback mechanism
        main_content = soup.find('div', {'class': 'main-content'})
        if main_content:
            img_tag = main_content.find('img')
            if img_tag and 'src' in img_tag.attrs:
                main_image = img_tag['src']

    # Get headline
    headline_tag = soup.find('h1')
    headline = headline_tag.text.strip() if headline_tag else None

    # Get byline and publication date from JSON-LD script tag
    script_tag = soup.find('script', type='application/ld+json')
    if script_tag:
        data = json.loads(script_tag.string)
        byline = data.get('creator')[0] if 'creator' in data and data['creator'] else None
        publication_date = data.get('datePublished')
    else:
        byline = None
        publication_date = None

    # Get image captions
    caption_tags = soup.find_all('figcaption')
    captions = [tag.text.strip() for tag in caption_tags]

    # Get article text
    paragraph_tags = soup.find_all('p')
    article_text = ' '.join([p.get_text() for p in paragraph_tags])

    return {
        "url": url,
        "headline": headline,
        "byline": byline,
        "main_image": main_image,
        "image_captions": captions,
        "article": article_text,
        "publication_date": publication_date
    }
