from langchain.llms import GigaChat  # Импорт из LangChain (нужен langchain-community для GigaChat)
from langchain.prompts import PromptTemplate
from .. import config  # Или конкретно: from ..config import GIGACHAT_CLIENT_ID, GIGACHAT_CLIENT_SECRET, etc.

# Инициализация GigaChat (нужен langchain-community, добавь в requirements если нужно: langchain-community)
llm = GigaChat(
    client_id=config.GIGACHAT_CLIENT_ID,
    client_secret=config.GIGACHAT_CLIENT_SECRET,
    scope=config.GIGACHAT_SCOPE
)

def generate_posts(article_data: dict) -> dict:
    prompt_template = PromptTemplate(
        input_variables=["title", "facts", "quotes", "source_url"],
        template="""
        На основе статьи "{title}":
        Факты: {facts}
        Цитаты: {quotes}
        
        Сгенерируй 3 поста для разных платформ с ссылкой на источник {source_url}:
        - Telegram: коротко, по делу, только факты. Публиковать сейчас.
        - VK: дружелюбно, с эмодзи, на "ты". Публиковать через 3-4 часа.
        - Бизнес-блог (VC): профессионально, акцент на бизнес-успех. Публиковать завтра утром.
        
        Добавь тайминг и стиль как указано.
        """
    )
    
    chain = prompt_template | llm
    response = chain.invoke({
        "title": article_data["title"],
        "facts": "\n".join(article_data["facts"]),
        "quotes": "\n".join(article_data["quotes"]),
        "source_url": article_data["source_url"]
    })
    
    # Парсим ответ в dict (упрощенно; в реале используй json parsing)
    posts = {
        "telegram": response.split("Telegram:")[1].split("VK:")[0].strip() if "Telegram:" in response else "",
        "vk": response.split("VK:")[1].split("Бизнес-блог:")[0].strip() if "VK:" in response else "",
        "blog": response.split("Бизнес-блог:")[1].strip() if "Бизнес-блог:" in response else ""
    }
    return posts
