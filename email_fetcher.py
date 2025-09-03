import os.path
import json
import base64
from email.utils import parsedate_to_datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from params import FALLBACK_EMAIL_COUNT

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CHECKPOINT_FILE = 'checkpoint.json'

def load_checkpoint():
    """Read checkpoint.json, create if doesn't exist"""
    if not os.path.exists(CHECKPOINT_FILE):
        checkpoint = {
            "last_processed_id": None,
            "last_processed_timestamp": None,
            "processed_ids": []
        }
        with open(CHECKPOINT_FILE, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        return checkpoint
    
    with open(CHECKPOINT_FILE, 'r') as f:
        return json.load(f)

def update_checkpoint(email_id, timestamp):
    """Update checkpoint after processing each email"""
    checkpoint = load_checkpoint()
    checkpoint['last_processed_id'] = email_id
    checkpoint['last_processed_timestamp'] = timestamp
    
    if email_id not in checkpoint['processed_ids']:
        checkpoint['processed_ids'].append(email_id)
    
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(checkpoint, f, indent=2)

def is_already_processed(email_id):
    """Check against processed_ids list"""
    checkpoint = load_checkpoint()
    return email_id in checkpoint['processed_ids']

def build_gmail_query(checkpoint):
    """Build query string for unread emails with timestamp filter"""
    query = "is:unread"
    
    if checkpoint and checkpoint.get('last_processed_timestamp'):
        query += f" after:{checkpoint['last_processed_timestamp']}"
    
    return query

def get_gmail_service():
    """Initialize and return Gmail service"""
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
        with open('token.json', 'w') as f:
            f.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def get_body(payload):
    """Finds and returns the plain text body of an email"""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                return part['body']['data']
    elif payload['mimeType'] == 'text/plain':
        return payload['body']['data']
    return ''

def extract_email_data(msg):
    """Extract email data into structured dict"""
    headers = msg['payload']['headers']
    
    # Extract header values
    subject = next((d['value'] for d in headers if d['name'] == 'Subject'), 'No Subject')
    sender = next((d['value'] for d in headers if d['name'] == 'From'), 'Unknown Sender')
    date = next((d['value'] for d in headers if d['name'] == 'Date'), '')
    
    # Extract sender email from "Name <email@domain.com>" format
    sender_email = sender
    if '<' in sender and '>' in sender:
        start = sender.find('<') + 1
        end = sender.find('>')
        sender_email = sender[start:end]
    
    # Extract body
    body_data = get_body(msg['payload'])
    body = ''
    if body_data:
        try:
            body = base64.urlsafe_b64decode(body_data).decode('utf-8')
        except Exception as e:
            print(f"Error decoding body for email {msg['id']}: {e}")
            body = ''
    
    # Convert date to RFC 3339 format for consistency
    parsed_date = date
    try:
        dt = parsedate_to_datetime(date)
        parsed_date = dt.isoformat()
    except Exception:
        parsed_date = date
    
    # Check if email is unread
    is_unread = 'UNREAD' in msg.get('labelIds', [])
    
    return {
        'email_id': msg['id'],
        'thread_id': msg['threadId'],
        'subject': subject,
        'sender': sender,
        'sender_email': sender_email,
        'body': body,
        'date': parsed_date,
        'is_unread': is_unread
    }

def fetch_emails_to_process(checkpoint):
    """Fetch both unread emails AND last X emails as fallback"""
    service = get_gmail_service()
    
    # Get all email IDs we need to check
    email_ids = set()
    
    # 1. Get unread emails
    query = build_gmail_query(checkpoint)
    result = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=100
    ).execute()
    
    unread_messages = result.get('messages', [])
    for msg in unread_messages:
        email_ids.add(msg['id'])
    
    # 2. Get last X emails regardless of read status
    result = service.users().messages().list(
        userId='me',
        maxResults=FALLBACK_EMAIL_COUNT
    ).execute()
    
    recent_messages = result.get('messages', [])
    for msg in recent_messages:
        email_ids.add(msg['id'])
    
    # 3. Fetch full details for all unique email IDs
    emails = []
    for email_id in email_ids:
        # Skip if already processed
        if is_already_processed(email_id):
            continue
            
        msg = service.users().messages().get(userId='me', id=email_id).execute()
        email_data = extract_email_data(msg)
        emails.append(email_data)
    
    # Sort by date (oldest first) for chronological processing
    emails.sort(key=lambda x: x['date'])
    return emails

def process_new_emails():
    """Main loop to process new emails"""
    checkpoint = load_checkpoint()
    emails = fetch_emails_to_process(checkpoint)
    
    print(f"Found {len(emails)} emails to process")
    
    for email in emails:
        # For now, just print the email info
        status = "UNREAD" if email['is_unread'] else "READ"
        print(f"[{status}] {email['subject']}")
        print(f"From: {email['sender']}")
        print(f"Date: {email['date']}")
        print(f"Body preview: {email['body'][:100]}...")
        print("-" * 50)
        
        # Update checkpoint after processing
        update_checkpoint(email['email_id'], email['date'])

if __name__ == '__main__':
    process_new_emails()