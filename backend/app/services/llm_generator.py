from langchain_community.llms import GigaChat  
from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  
from dotenv import load_dotenv  
import os  
import requests  
import uuid  
import json  
import logging  

load_dotenv()  
logging.basicConfig(level=logging.ERROR)  

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
        'Authorization': f'Basic {auth_key.strip()}'  
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

def fallback_posts(article_data: dict) -> dict:  
    title = article_data.get("title", "Новость")  
    facts = ' '.join(article_data.get("facts", []))  
    quotes = ' '.join(article_data.get("quotes", []))  
    numbers = ', '.join(article_data.get("numbers", []))  
    full_text = article_data.get("full_text", "")[:800]  
    source_url = article_data.get("source_url", "")  
    telegram = f"⚡ Срочно! {title}"  
    if facts: telegram += f". Факты: {facts}"  
    if numbers: telegram += f". Цифры: {numbers}"  
    if quotes: telegram += f". Цитаты: {quotes}"  
    if full_text: telegram += f". {full_text}"  
    telegram += f". Полный материал: {source_url}"  

    vk = f"Привет, друзья! 😊 {title}"  
    if facts: vk += f". Факты: {facts}"  
    if numbers: vk += f". {numbers}"  
    if quotes: vk += f". {quotes}"  
    if full_text: vk += f". {full_text}"  
    vk += f". Что думаете? 🚀 Источник: {source_url}"  

    blog = f"Стратегический обзор: {title}"  
    if facts: blog += f". Факты: {facts}"  
    if numbers: blog += f". Метрики: {numbers}"  
    if quotes: blog += f". Цитата: {quotes}"  
    if full_text: blog += f". {full_text}"  
    blog += f". Читайте: {source_url}"  

    return {"telegram": telegram, "vk": vk, "blog": blog}  

def generate_posts(article_data: dict) -> dict:  
    title = article_data.get("title", "Новость")  
    source_url = article_data.get("source_url", "")  
    prompt_template = PromptTemplate(  
        input_variables=["title", "source_url"],  
        template="""  
Ты PR-агент. На основе заголовка новости "{title}" сгенерируй 3 полноценных поста (каждый 400-600 символов, coherentный нарратив в 2–3 раза длиннее заголовка, с вымышленными деталями/фактами/метриками/цитатами для полноты):  
- Telegram: коротко, по делу, только факты, с ⚡, начать с "Срочно!". Закончить ссылкой: {source_url}  
- VK: дружелюбно, с 😊🚀, на "ты", вопрос к аудитории. Начать с "Привет, друзья!". Закончить ссылкой.  
- Бизнес-блог VC: профессионально, акцент на бизнес-успех/метрики. Начать с "Стратегический обзор:". Закончить ссылкой.  

Верни ТОЛЬКО JSON: {{"telegram": "текст", "vk": "текст", "blog": "текст"}}  
        """  
    )  
    chain = LLMChain(llm=llm, prompt=prompt_template)  
    try:  
        response = chain.run(title=title, source_url=source_url)  
        response = response.strip().replace('```json', '').replace('```', '')  
        posts = json.loads(response)  
    except:  
        posts = {  
            "telegram": f"⚡ Срочно! {title}. Подробности в материале: {source_url}",  
            "vk": f"Привет, друзья! 😊 {title}. Что думаете? 🚀 Источник: {source_url}",  
            "blog": f"Стратегический обзор: {title}. Это влияет на рынок. Читайте: {source_url}"  
        }  
    return posts
