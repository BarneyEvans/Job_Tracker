import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
import base64

# Define the scope for our application
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """
    Authenticates with the Gmail API and returns a service object.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def read_and_write_to_json(current_service):
    with open("checkpoint.json", "r") as f:
        checkpoint_data = json.load(f)

    # USING SETS TO MAKE THIS SHIT QUICK ASF
    all_messages_info = current_service.users().messages().list(userId='me').execute()
    new_id_set = set([msg['id'] for msg in all_messages_info['messages']])
    processed_id_set = set(checkpoint_data['processed_ids'])
    unprocessed_ids = list(new_id_set - processed_id_set)
    
    return unprocessed_ids

def get_subject(message):
    for info in message["payload"]["headers"]:
        if info["name"] == "Subject":
            return info["value"]
    return "No Subject"

def get_body(message):
    for info in message["payload"]["parts"]:
        if info["mimeType"] == "text/plain":
            data = info["body"]["data"]
            body = base64.urlsafe_b64decode(data)
            return body.decode("utf-8")
    return "No Content"

def get_sender_email(message):
    for info in message["payload"]["headers"]:
        if info["name"] == "From":
            return info["value"]
    return "No Sender Email"   

def get_date(message):
    for info in message["payload"]["headers"]:
        if info["name"] == "Date":
            return info["value"]
    return "No Date"

def get_content(ids, current_service):
    # A dictionary of ids, each containing subject and content
    email_content = {}
    for id in ids:
        current_message = current_service.users().messages().get(userId="me", id=id).execute()
        #print(current_message)
        #print("-" * 100)
        email_content[id] = {}
        email_content[id]["Subject"] = get_subject(current_message)
        email_content[id]["Content"] = get_body(current_message)
        email_content[id]["Sender_Email"] = get_sender_email(current_message)
        email_content[id]["Date"] = get_date(current_message)
    return email_content

def retrieve_gmails():
    service = get_gmail_service()
    ids_for_processing = read_and_write_to_json(service)
    content = get_content(ids_for_processing, service)
    return content

    
# This part is just for testing our function directly
if __name__ == '__main__':
    test = retrieve_gmails()
    with open("emails.json", "w", encoding="utf-8") as f:
        json.dump(test, f, indent=4, ensure_ascii=False)
    print("Saved to emails.json")