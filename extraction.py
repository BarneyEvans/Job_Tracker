import requests
from params import (
    data_extraction_prompt
    )
from gmail_api import retrieve_gmails
from datetime import datetime
from llm_call import send_request, format_response


def extract_information():
    emails = retrieve_gmails()
    necessary_data = {}

    for email_id in emails:
        email_subject = emails[email_id]["Subject"]
        email_content = emails[email_id]["Content"]
        prompt = data_extraction_prompt(email_subject, email_content)
        output = send_request(prompt, ollama=True)
        try:
            out_json = format_response(output)
            parsed_email = eval(out_json)
            if parsed_email["status"].upper() != "IRRELEVANT":
                if parsed_email["status"].upper() != "UNSURE":
                    parsed_email["date"] = datetime.strptime(emails[email_id]["Date"], "%a, %d %b %Y %H:%M:%S %z").isoformat()
                    parsed_email["sender_email"] = emails[email_id]["Sender_Email"]
                    parsed_email["subject"] = emails[email_id]["Subject"]
                    parsed_email["content"] = emails[email_id]["Content"]
                    if parsed_email["status"] == "awaiting_response":
                        parsed_email["status"] = "action_required"
                    if parsed_email["substate"] == "awaiting_response":
                        parsed_email["substate"] = "action_required"
                    necessary_data[email_id] = parsed_email
        except:
            continue
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
        print(f"  Stage: {processed_emails[email_id]['status']}")
        print(f"  Position: {processed_emails[email_id]['position']}")
        print(f"  Date: {processed_emails[email_id]["date"]}")
        # print(f"  Content: {processed_emails[email_id]['content']}")
        print("-" * 25 + "\n")