import requests  
import json  
import time  
from dotenv import load_dotenv  
import os  
load_dotenv()  

API_URL = "https://api-key.fusionbrain.ai/"  
API_KEY = os.getenv("KANDINSKY_API_KEY")  
SECRET_KEY = os.getenv("KANDINSKY_SECRET_KEY")  
AUTH_HEADERS = {  
    'X-Key': f'Key {API_KEY}',  
    'X-Secret': f'Secret {SECRET_KEY}',  
}  

def get_pipeline_id():  
    response = requests.get(API_URL + 'key/api/v1/pipelines', headers=AUTH_HEADERS)  
    if response.status_code == 200:  
        return response.json()[0]['id']  
    raise ValueError("Ошибка получения pipeline")  

PIPELINE_ID = get_pipeline_id()  

def generate_image(prompt: str) -> str:  
    if not prompt: return "https://via.placeholder.com/1024?text=Error"  
    params = {  
        "type": "GENERATE",  
        "numImages": 1,  
        "width": 1024,  
        "height": 1024,  
        "generateParams": {"query": f"Креативная иллюстрация к новости: {prompt[:500]}, стиль современный PR, яркий"}  
    }  
    data = {  
        'pipeline_id': (None, PIPELINE_ID),  
        'params': (None, json.dumps(params), 'application/json')  
    }  
    response = requests.post(API_URL + 'key/api/v1/pipeline/run', headers=AUTH_HEADERS, files=data)  
    if response.status_code != 200:  
        return "https://via.placeholder.com/1024?text=Error"  
    uuid_val = response.json()['uuid']  
    attempts = 30  
    while attempts > 0:  
        status_res = requests.get(API_URL + f'key/api/v1/pipeline/status/{uuid_val}', headers=AUTH_HEADERS)  
        data = status_res.json()  
        if data['status'] == 'DONE':  
            if data.get('result', {}).get('censored'):  
                return "https://via.placeholder.com/1024?text=Censored"  
            return f"data:image/jpeg;base64,{data['result']['files'][0]}"  
        time.sleep(10)  
        attempts -= 1  
    return "https://via.placeholder.com/1024?text=Timeout"  
