import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
import base64
from database import read_last_timestamp, write_last_timestamp

# Define the scope for our application
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """
    Authenticates with the Gmail API and returns a service object.
    """
    creds = None
    if os.path.exists('backend/token.json'):
        creds = Credentials.from_authorized_user_file('backend/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'backend/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('backend/token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_new_email_ids(current_service, last_timestamp):
    latest_timestamp = last_timestamp
    new_ids = []
    all_messages_info = current_service.users().messages().list(userId='me').execute()
    messages = []
    for msg in all_messages_info.get('messages', []):
        msg_detail = current_service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata'   # faster than 'full' since you just need metadata
        ).execute()
        
        messages.append({
            "id": msg['id'],
            "timestamp": int(msg_detail['internalDate'])  # in ms since epoch
        })
    for msg in messages:
        if msg["timestamp"] > last_timestamp:
            new_ids.append(msg["id"])
            if msg["timestamp"] > latest_timestamp:
                latest_timestamp = msg["timestamp"]
    return new_ids, latest_timestamp



def get_subject(message):
    for info in message["payload"]["headers"]:
        if info["name"] == "Subject":
            return info["value"]
    return "No Subject"

def get_body(message):
    # with open("text.json", "w", encoding="utf-8") as f:
    #     json.dump(message["payload"]["parts"], f, indent=4, ensure_ascii=False)
    # quit()
    for info in message["payload"]["parts"]:
        if info["mimeType"] == "text/plain":
            data = info["body"]["data"]
            body = base64.urlsafe_b64decode(data)
            return body.decode("utf-8")
        if info["mimeType"] == "text/html":
            data = info["body"]["data"]
            html = base64.urlsafe_b64decode(data).decode("utf-8")
            return html
        if info["mimeType"] == "multipart/alternative":
            for part in info["parts"]:
                if part["mimeType"] == "text/plain":
                    data = part["body"]["data"]
                    body = base64.urlsafe_b64decode(data)
                    return body.decode("utf-8")
                if part["mimeType"] == "text/html":
                    data = part["body"]["data"]
                    html = base64.urlsafe_b64decode(data).decode("utf-8")
                    return html

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
        print(get_subject(current_message))
        #print("-" * 100)
        email_content[id] = {}
        email_content[id]["Subject"] = get_subject(current_message)
        email_content[id]["Content"] = get_body(current_message)
        email_content[id]["Sender_Email"] = get_sender_email(current_message)
        email_content[id]["Date"] = get_date(current_message)
    return email_content

def retrieve_gmails():
    service = get_gmail_service()
    timestamp = read_last_timestamp()
    ids_for_processing, latest_timestamp = get_new_email_ids(service, timestamp)
    write_last_timestamp(latest_timestamp)
    content = get_content(ids_for_processing, service)
    return content

    
# This part is just for testing our function directly
if __name__ == '__main__':
    test = retrieve_gmails()
    with open("backend/emails.json", "w", encoding="utf-8") as f:
        json.dump(test, f, indent=4, ensure_ascii=False)
    print("Saved to backend/emails.json")