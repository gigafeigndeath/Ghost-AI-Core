import requests  
from bs4 import BeautifulSoup  
from urllib.parse import urlparse, urlunparse  

HEADERS = {  
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"  
}  

def parse_article(url: str) -> dict:  
    parsed = urlparse(url)  
    clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))  
    try:  
        response = requests.get(url, headers=HEADERS, timeout=15)  
        response.raise_for_status()  
    except:  
        return {"title": "Ошибка загрузки заголовка", "source_url": clean_url}  
    soup = BeautifulSoup(response.text, 'html.parser')  
    title = (soup.find('meta', {'property': 'og:title'})['content'].strip() if soup.find('meta', {'property': 'og:title'}) else  
             soup.find('h1').text.strip() if soup.find('h1') else  
             soup.title.text.strip() if soup.title else "Без заголовка")  
    return {"title": title, "source_url": clean_url}  
