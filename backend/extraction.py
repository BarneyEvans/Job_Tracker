import requests
from params import (
    data_extraction_prompt
    )
from gmail_api import retrieve_gmails
from database import fetch_companies
from datetime import datetime
from llm_call import send_request, format_response
from dateutil import parser


def extract_information(user_id):
    emails, latest_timestamp = retrieve_gmails(user_id)
    current_companies = fetch_companies(user_id)
    necessary_data = {}

    for email_id in emails:
        email_subject = emails[email_id]["Subject"]
        email_content = emails[email_id]["Content"]
        print("Email content", email_content)
        prompt = data_extraction_prompt(current_companies, email_subject, email_content)
        print("Prompt generated successfully")
        output = send_request(prompt, ollama=False)
        if output == "":
            print(email_subject, ":  Not relevant")
            continue
        try:
            out_json = format_response(output)
            parsed_email = eval(out_json)
            if parsed_email["status"].upper() != "IRRELEVANT":
                if parsed_email["status"].upper() != "UNSURE":
                    date_str = emails[email_id].get("Date")
                    if date_str and date_str.lower() != "no date":
                        try:
                            parsed_email["date"] = parser.parse(date_str).isoformat()
                        except Exception:
                            parsed_email["date"] = None
                    else:
                        parsed_email["date"] = None
                    parsed_email["sender_email"] = emails[email_id]["Sender_Email"]
                    parsed_email["subject"] = emails[email_id]["Subject"]
                    parsed_email["content"] = emails[email_id]["Content"]
                    parsed_email["thread_id"] = emails[email_id].get("ThreadId")
                    parsed_email["message_id"] = emails[email_id].get("MessageId")
                    parsed_email["in_reply_to"] = emails[email_id].get("InReplyTo")
                    if parsed_email["status"] == "awaiting_response":
                        parsed_email["status"] = "action_required"
                    if parsed_email["substate"] == "awaiting_response":
                        parsed_email["substate"] = "action_required"
                    necessary_data[email_id] = parsed_email
        except Exception as e:
            print(f"Error processing email ID {email_id}: {e}")
            continue
    return necessary_data, latest_timestamp



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
        print(f"  Date: {processed_emails[email_id]['date']}")
        # print(f"  Content: {processed_emails[email_id]['content']}")
        print("-" * 25 + "\n")
