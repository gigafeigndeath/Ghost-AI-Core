from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def parse_with_selenium(url: str) -> str:
    """Парсер на Selenium для динамических сайтов — возвращает текст статьи."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(5)  # ждём загрузки JS
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for script in soup(["script", "style", "header", "footer", "nav", "aside"]):
            script.decompose()

        text = soup.get_text(separator=' ', strip=True)
        driver.quit()
        return text[:5000]
    except Exception as e:
        return f"Ошибка selenium-парсинга: {str(e)}"
