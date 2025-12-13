from langchain_community.llms import GigaChat
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import requests
import uuid
import base64
import json

load_dotenv()

def get_gigachat_token():
    auth_key = os.getenv("GIGACHAT_AUTH_KEY")
    if not auth_key:
        raise ValueError("GIGACHAT_AUTH_KEY not set in .env")
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    payload = "scope=GIGACHAT_API_PERS"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),
        'Authorization': f'Basic {auth_key.strip()}'  # strip() фикс пробелов
    }
    response = requests.post(url, headers=headers, data=payload, verify=False)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise ValueError(f"Ошибка получения токена: {response.text}")

llm = GigaChat(
    access_token=get_gigachat_token(),
    model="GigaChat",
    verify_ssl_certs=False
)

def generate_posts(article_data: dict) -> dict:
    title = article_data.get("title", "Новость")
    facts = article_data.get("facts", [])
    quotes = article_data.get("quotes", [])
    source_url = article_data.get("source_url", "")

    prompt_template = PromptTemplate(
        input_variables=["title", "facts", "quotes", "source_url"],
        template="""
Ты PR-агент. На основе статьи с заголовком "{title}", фактами {facts}, цитатами {quotes} и ссылкой на источник {source_url} сгенерируй 3 поста:

1. Для Telegram (публиковать сейчас, коротко, по делу, только факты, с ⚡ и обязательной ссылкой на источник):
2. Для VK (публиковать через 3-4 часа, дружелюбно, с эмодзи 😊, на "ты", с вопросом к аудитории, обязательной ссылкой на источник):
3. Для бизнес-блога VC (публиковать завтра утром, профессионально, акцент на бизнес-успех и развитие, с цитатой, обязательной ссылкой на источник):

Верни в формате JSON без лишнего текста:
{{"telegram": "текст поста", "vk": "текст поста", "blog": "текст поста"}}
"""
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    response = chain.run(title=title, facts=facts, quotes=quotes, source_url=source_url)

    try:
        posts = json.loads(response)
    except json.JSONDecodeError:
        posts = {
            "telegram": "⚡ Факты из статьи: " + " ".join(facts) + " Источник: " + source_url,
            "vk": "Привет! 😊 " + title + " — что думаете? Источник: " + source_url,
            "blog": "Профессиональный обзор: " + (quotes[0] if quotes else "") + " Источник: " + source_url
        }

    return posts
