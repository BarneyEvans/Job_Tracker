import requests
from params import MODEL_NAME, OLLAMA_ENDPOINT, generate_classification_prompt, generate_info_extractor_prompt
from gmail_api import retrieve_gmails

def information_extraction():
    emails = retrieve_gmails()
    for email in emails:
        email_s = emails[email]["Subject"]
        email_b = emails[email]["Content"]
        prompt = generate_classification_prompt(email_s, email_b)

        #First Check for classification
        data = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
        classification_response = requests.post(OLLAMA_ENDPOINT, json=data)
        unfiltered_result_1 = classification_response.json()['response']
        classification_result = unfiltered_result_1.split("</think>")[-1]
        emails[email]["Classification"] = classification_result

        #print(classification_result)

        #Second Check for general information extraction
        if "irrelevant" not in classification_result.lower() and "unsure" not in classification_result.lower():
            email_subject = emails[email]["Subject"]
            email_content = emails[email]["Content"]
            prompt = generate_info_extractor_prompt(email_subject, email_content)
            data = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
            general_info_response = requests.post(OLLAMA_ENDPOINT, json=data)
            unfiltered_result_2 = general_info_response.json()['response']
            general_info_result = unfiltered_result_2.split("</think>")[-1]
            emails[email]["Extracted_Info"] = general_info_result
        else:
            emails[email]["Extracted_Info"] = "None"
        
    return emails

if __name__ == '__main__':
    processed_emails = information_extraction()

    print("\n--- PROCESSING COMPLETE ---")
    print(f"Found and processed {len(processed_emails)} new emails.\n")

    # Loop through each email in the results
    for email_id, email_data in processed_emails.items():
        print(f"--- Email ID: {email_id} ---")
        print(f"  Subject: {email_data['Subject']}")
        print(f"  Classification: {email_data['Classification']}")
        
        # Now let's handle the extracted info
        extracted_info = email_data.get('Extracted_Info', 'None')
        if extracted_info and extracted_info != 'None':
            print("  Extracted Information:")
            # The model returns a single string, so we split it by lines
            lines = extracted_info.strip().splitlines()
            for line in lines:
                print(f"    - {line.strip()}")
        else:
            print("  Extracted Information: None")
            
        print("-" * 25 + "\n") # Add a nice separator
