from app.parsers.bs4_parser import parse_with_bs4
from app.parsers.selenium_parser import parse_with_selenium

def read_article(url: str, method: str = "bs4"):
    if method == "bs4":
        return parse_with_bs4(url)
    elif method == "selenium":
        return parse_with_selenium(url)
    else:
        raise ValueError("Unknown parser method")