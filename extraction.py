import requests
from params import MODEL_NAME, OLLAMA_ENDPOINT, EXTRACTION_STATES, generate_classification_prompt, generate_single_extraction_prompt
from gmail_api import retrieve_gmails


def get_result(data_ting):
    classification_response = requests.post(OLLAMA_ENDPOINT, json=data_ting)
    response = classification_response.json()['response']
    result = response.split("</think>")[-1]
    return result



def information_extraction():
    emails = retrieve_gmails()
    useful_emails = {}

    for email in emails:
        email_subject = emails[email]["Subject"]
        email_content = emails[email]["Content"]
        prompt = generate_classification_prompt(email_subject, email_content)

        #First Check for classification
        data = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
        emails[email]["Classification"] = get_result(data).strip()

        if "irrelevant" not in emails[email]["Classification"].lower():
            useful_emails[email] = emails[email]
    
    for email in useful_emails:
        email_subject = emails[email]["Subject"]
        email_content = emails[email]["Content"]
        #Second Check for general information extraction
        for state in EXTRACTION_STATES:
            prompt = generate_single_extraction_prompt(email_subject, email_content, state)
            data = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
            useful_emails[email][state] = get_result(data).strip()

    return useful_emails

if __name__ == '__main__':
    processed_emails = information_extraction()
    # print(processed_emails)

    print("\n--- PROCESSING COMPLETE ---")
    print(f"Found and processed {len(processed_emails)} new emails.\n")

    # Loop through each email in the results
    for email_id, email_data in processed_emails.items():
        print(f"--- Email ID: {email_id} ---")
        print(f"  Subject: {email_data['Subject']}")
        print(f"  Classification: {email_data['Classification']}")
        
        # Check if the first extraction state exists (a good sign that extraction was run)
        if "Company Name" in email_data:
            print("  Extracted Information:")
            # Loop through your EXTRACTION_STATES to print each one
            for state in EXTRACTION_STATES:
                # Use .get() to safely access the key in case it's missing
                info = email_data.get(state, "Not Found").strip()
                print(f"    - {state}: {info}")
        else:
            print("  Extracted Information: None")
            
        print("-" * 25 + "\n")