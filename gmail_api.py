import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_body(payload):
    """
    Finds and returns the plain text body of an email.
    Searches through the payload parts for the 'text/plain' mimeType.
    """
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                return part['body']['data']
    # If the email is not multipart and is plain text
    elif payload['mimeType'] == 'text/plain':
        return payload['body']['data']
    return ''

def main():
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
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    result = service.users().messages().list(userId='me', maxResults=5).execute()
    messages = result.get('messages', [])

    if not messages:
        print("No messages found.")
    else:
        print("Fetching your 5 most recent emails...\n")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            
            headers = msg['payload']['headers']
            subject = next((d['value'] for d in headers if d['name'] == 'Subject'), 'No Subject')
            sender = next((d['value'] for d in headers if d['name'] == 'From'), 'Unknown Sender')

            body_data = get_body(msg['payload'])
            body = ''
            if body_data:
                body = base64.urlsafe_b64decode(body_data).decode('utf-8')
            
            print(f"From: {sender}")
            print(f"Email ID: {message['id']}")
            print(f"Subject: {subject}")
            print("Body:")
            print(f"{body[:300]}...") # Print first 300 characters of the body
            print("-" * 50)

if __name__ == '__main__':
    main()