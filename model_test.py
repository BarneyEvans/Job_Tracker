import requests
from params import model_name, ollama_endpoint, prompt, states

#To prevent too many loops
counter = 0


data = {"model": model_name, "prompt": prompt, "stream": False}
response = requests.post(ollama_endpoint, json=data)
result = response.json()['response']
# while result not in states and counter < 3:
#     response = requests.post(ollama_endpoint, json=data)
#     result = response.json()['response']
#     counter = counter + 1

with open("output.txt", "w") as f:
    f.write(result)

print(result)