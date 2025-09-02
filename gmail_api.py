import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# The SCOPES define the permissions your script is asking for.
# 'readonly' is safe as it doesn't allow the script to change anything.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """
    Authenticates with the Gmail API and lists the 5 most recent emails.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials, let the user log in.
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

    # Build the Gmail service
    service = build('gmail', 'v1', credentials=creds)

    # --- Start of the new part ---

    # 1. Get a list of the 5 most recent message IDs
    result = service.users().messages().list(userId='me', maxResults=5).execute()
    messages = result.get('messages', [])

    if not messages:
        print("No new messages found.")
    else:
        print("Your 5 most recent emails:\n")
        for message in messages:
            # 2. Get the full message details for each ID
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            
            # 3. Find the 'Subject' and 'From' headers
            headers = msg['payload']['headers']
            subject = next((d['value'] for d in headers if d['name'] == 'Subject'), 'No Subject')
            sender = next((d['value'] for d in headers if d['name'] == 'From'), 'Unknown Sender')

            print(f"From: {sender}")
            print(f"Subject: {subject}\n" + "-"*20)

if __name__ == '__main__':
    main()