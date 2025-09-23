import requests
from params import (
    MODEL_NAME, 
    OLLAMA_ENDPOINT, 
    EXTRACTION_STATES, 
    generate_classification_prompt, 
    generate_single_extraction_prompt, 
    data_extraction_prompt
    )
from gmail_api import retrieve_gmails

# Replaced by parse_email
# def get_result(prompt): 
#     options = {"temperature": 0}
#     data = {"model": MODEL_NAME, "prompt": prompt, "stream": False, "options": options}
#     classification_response = requests.post(OLLAMA_ENDPOINT, json=data)
#     response = classification_response.json()['response']
#     result = response.split("</think>")[-1]
#     return result


# Replaced by extract_information
# def information_extraction(): 
#     emails = retrieve_gmails()
#     useful_emails = {}

#     for email in emails:
#         email_subject = emails[email]["Subject"]
#         email_content = emails[email]["Content"]
#         prompt = generate_classification_prompt(email_subject, email_content)

#         #First Check for classification
        
#         emails[email]["Classification"] = get_result(prompt).strip()

#         if "irrelevant" not in emails[email]["Classification"].lower():
#             useful_emails[email] = emails[email]
    
#     for email in useful_emails:
#         email_subject = emails[email]["Subject"]
#         email_content = emails[email]["Content"]
#         #Second Check for general information extraction
#         for state in EXTRACTION_STATES:
#             prompt = generate_single_extraction_prompt(email_subject, email_content, state)
#             useful_emails[email][state] = get_result(prompt).strip()

#     return useful_emails

def parse_email(prompt):
    options = {"temperature": 0}
    data = {"model": MODEL_NAME, "prompt": prompt, "stream": False, "options": options}
    classification_response = requests.post(OLLAMA_ENDPOINT, json=data)
    response = classification_response.json()['response']
    result = response.split("</think>")[-1]
    return result

def extract_information():
    emails = retrieve_gmails()
    necessary_data = {}

    for email_id in emails:
        email_subject = emails[email_id]["Subject"]
        email_content = emails[email_id]["Content"]
        prompt = data_extraction_prompt(email_subject, email_content)
        out_json = parse_email(prompt)
        parsed_email = eval(out_json)
        if parsed_email["stage"].upper() != "IRRELEVANT":
            if parsed_email["stage"].upper() != "UNSURE":
                parsed_email["date"] = emails[email_id]["Date"]
                parsed_email["sender_email"] = emails[email_id]["Sender_Email"]
                parsed_email["subject"] = emails[email_id]["Subject"]
                necessary_data[email_id] = parsed_email
    return necessary_data



if __name__ == '__main__':
    processed_emails = extract_information()
    # print(processed_emails)

    print("\n--- PROCESSING COMPLETE ---")
    print(f"Found and processed {len(processed_emails)} new emails.\n")

    # Loop through each email in the results
    for email_id in processed_emails.keys():
        value = processed_emails[email_id]
        print(f"--- Email ID: {email_id} ---")
        print(f"  Subject: {processed_emails[email_id]['subject']}")
        print(f"  Company: {processed_emails[email_id]['company']}")
        print(f"  Job Title: {processed_emails[email_id]['job_title']}")
        print(f"  Stage: {processed_emails[email_id]['stage']}")
        print(f"  Stage: {processed_emails[email_id]['position']}")
        print("-" * 25 + "\n")