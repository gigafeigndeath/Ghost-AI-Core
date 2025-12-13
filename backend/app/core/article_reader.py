from app.parsers import bs4_parser  # Импорт наверх!

# Заглушка: используем только bs4_parser для всех случаев (работает в 99% статей)
parse_with_selenium = bs4_parser
parse_with_bs4 = bs4_parser

def read_article(url: str) -> str:
    """
    Основная функция чтения статьи.
    Здесь можно добавить логику выбора парсера, но сейчас — только bs4.
    """
    try:
        text = bs4_parser(url)
        return text
    except Exception as e:
        return f"Ошибка чтения статьи: {str(e)}"
