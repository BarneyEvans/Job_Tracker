import requests
from params import model_name, ollama_endpoint, prompt

data = {"model": model_name, "prompt": prompt, "stream": False}
response = requests.post(ollama_endpoint, json=data)
result = response.json()['response']

with open("output.txt", "w") as f:
    f.write(result)

print(result)