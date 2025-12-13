import requests
from bs4 import BeautifulSoup

def parse_article(url: str) -> dict:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Вычлениваем ключевые элементы (адаптируй под реальные статьи)
    title = soup.find('title').text if soup.find('title') else "No title"
    facts = [p.text for p in soup.find_all('p')[:5]]  # Первые 5 параграфов как факты
    quotes = [blockquote.text for blockquote in soup.find_all('blockquote')]
    
    return {
        "title": title,
        "facts": facts,
        "quotes": quotes,
        "source_url": url
    }
