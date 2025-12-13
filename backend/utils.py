import requests
from bs4 import BeautifulSoup
import time
import base64
import os
import json

def get_gigachat_token():
    url = "https://gigachat.devices.sberbank.ru/api/v2/oauth"
    auth_key = os.getenv("GIGACHAT_AUTH_KEY")  # Base64-encoded authorization key from Sber Studio
    headers = {
        "Authorization": f"Basic {auth_key}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = "scope=GIGACHAT_API_PERS"
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def call_llm(prompt):
    token = get_gigachat_token()
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "GigaChat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 512
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def generate_image(prompt):
    api_key = os.getenv("FUSIONBRAIN_API_KEY")
    secret_key = os.getenv("FUSIONBRAIN_SECRET_KEY")
    base_url = "https://api-key.fusionbrain.ai/"
    headers = {
        "X-Key": f"Key {api_key}",
        "X-Secret": f"Secret {secret_key}"
    }

    # Get pipeline ID (Kandinsky is the first one)
    pipelines_resp = requests.get(base_url + "key/api/v1/pipelines", headers=headers)
    pipelines_resp.raise_for_status()
    pipeline_id = pipelines_resp.json()[0]["id"]

    # Prepare params
    params = {
        "type": "GENERATE",
        "numImages": 1,
        "width": 1024,
        "height": 1024,
        "generateParams": {"query": prompt}
    }

    # Submit generation request
    files = {
        "pipeline_id": (None, pipeline_id),
        "params": (None, json.dumps(params), "application/json")
    }
    run_resp = requests.post(base_url + "key/api/v1/pipeline/run", headers=headers, files=files)
    run_resp.raise_for_status()
    uuid = run_resp.json()["uuid"]

    # Poll for result
    while True:
        status_resp = requests.get(base_url + f"key/api/v1/pipeline/status/{uuid}", headers=headers)
        status_resp.raise_for_status()
        result = status_resp.json()
        if result["status"] == "DONE":
            image_b64 = result["result"]["files"][0]
            return f"data:image/jpeg;base64,{image_b64}"
        elif result["status"] == "FAIL":
            raise ValueError(f"Generation failed: {result.get('errorDescription', 'Unknown error')}")
        time.sleep(5)  # Wait 5 seconds before next poll

def parse_article(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string if soup.title else "No title"
    content = "\n".join(p.get_text() for p in soup.find_all('p'))
    return {"title": title, "content": content}

def generate_posts(url):
    article = parse_article(url)
    content = article["content"]
    source_link = f"Источник: {url}"
    platforms = {
        "telegram": {
            "style": "коротко, по делу, только факты",
            "timing": "сейчас",
            "prefix": "⚡ "
        },
        "vk": {
            "style": "дружелюбно, с эмодзи, «на ты» к аудитории",
            "timing": "через 3-4 часа",
            "prefix": ""
        },
        "business_blog": {
            "style": "профессионально, с акцентом на бизнес-успех и развитие",
            "timing": "завтра утром",
            "prefix": ""
        }
    }
    posts = {}
    for platform, info in platforms.items():
        llm_prompt = f"На основе статьи: {content}\nСоздай пост для {platform} в стиле: {info['style']}. Добавь ссылку на источник в конце. Краткий."
        text = info["prefix"] + call_llm(llm_prompt) + f"\n{source_link}"
        image_prompt = f"Креативная иллюстрация к новости: {article['title']}"
        image_url = generate_image(image_prompt)
        posts[platform] = {
            "text": text,
            "image_url": image_url,
            "timing": info["timing"]
        }
    return posts
