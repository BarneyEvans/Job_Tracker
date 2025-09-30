import requests
from params import (
    MODEL_NAME, 
    OLLAMA_ENDPOINT, 
    )
from openai import OpenAI
import os
from dotenv import load_dotenv

def send_request(prompt, ollama=True):
    if ollama:
        options = {"temperature": 0}
        data = {"model": MODEL_NAME, "prompt": prompt, "stream": False, "options": options}
        classification_response = requests.post(OLLAMA_ENDPOINT, json=data)
        response = classification_response.json()['response']
        result = response.split("</think>")[-1]
    else:
        load_dotenv()

        api_key = os.getenv('CHATGPT_API_KEY')
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-5-nano",
            input=prompt,
            # temperature=0.0,
            service_tier="flex",
        )
        result = response.output_text
    return result

def format_response(response):
    start_index = response.index("{")
    end_index = response.index("}")
    print(response[start_index:end_index+1])
    return response[start_index:end_index+1]