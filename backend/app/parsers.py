from newspaper import Article

def newspaper_parser(url: str) -> str:
    """Другой вариант парсинга — newspaper3k: автоматически выжимает чистый текст статьи."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        # Чистый текст + заголовок + автор + дата (идеально для рерайта)
        text = article.text.strip()
        title = article.title.strip()
        authors = ", ".join(article.authors)
        date = article.publish_date.strftime("%d.%m.%Y") if article.publish_date else "неизвестно"
        
        full_text = f"Заголовок: {title}\nАвторы: {authors}\nДата: {date}\n\n{text}"
        return full_text[:8000]  # ограничиваем для LLM
    except Exception as e:
        return f"Ошибка newspaper-парсинга: {str(e)} (fallback на пустой текст)"

# Если есть get_parser — верни newspaper_parser
def get_parser(parser_type: str = "newspaper"):
    return newspaper_parser
