from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def parse_with_selenium(url: str):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    content = driver.page_source
    driver.quit()
    return content  # Можно дальше парсить с BS4