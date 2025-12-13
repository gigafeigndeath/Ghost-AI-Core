from app.parsers import get_parser

def read_article(url: str) -> str:
    parser = get_parser()  # фабрика возвращает bs4_parser или другой
    return parser(url)
