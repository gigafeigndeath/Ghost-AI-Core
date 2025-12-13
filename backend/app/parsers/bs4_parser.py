import requests
from bs4 import BeautifulSoup

def parse_with_bs4(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()