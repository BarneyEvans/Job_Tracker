import requests
from params import MODEL_NAME, OLLAMA_ENDPOINT, generate_classification_prompt
from gmail_api import retrieve_gmails

#To prevent too many loops
counter = 0

def classifcation_loop():
    classified_emails = {}
    emails = retrieve_gmails()
    for email in emails:
        email_s = emails[email]["Subject"]
        email_b = emails[email]["Content"]
        prompt = generate_classification_prompt(email_s, email_b)
        data = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
        response = requests.post(OLLAMA_ENDPOINT, json=data)
        result = response.json()['response']

        #May need to implement a checker to remove reasoning model thoughts

        classified_emails[email] = result
    print(classified_emails)
    return classified_emails

if __name__ == '__main__':
    test = classifcation_loop()
