from .bs4_parser import parse_with_bs4
from .selenium_parser import parse_with_selenium

def get_parser(method: str):
    if method == "bs4":
        return parse_with_bs4
    elif method == "selenium":
        return parse_with_selenium
    else:
        raise ValueError("Unknown parser")