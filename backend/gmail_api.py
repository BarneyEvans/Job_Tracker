import html
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
import base64
import webbrowser
from database import read_last_timestamp, write_creds, read_creds
from bs4 import BeautifulSoup
from datetime import datetime, timezone

# Define the scope for our application
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# def get_gmail_service():
#     """
#     Authenticates with the Gmail API and returns a service object.
#     """
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#     creds_path = os.path.join(BASE_DIR, "credentials.json")
#     token_path = os.path.join(BASE_DIR, "token.json")

#     creds = None
#     if os.path.exists(token_path):
#         creds = Credentials.from_authorized_user_file(token_path, SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 creds_path, SCOPES, redirect_uri="http://localhost:5173/")
#             creds = flow.run_local_server(port=5173)
#         # Save the credentials for the next run
#         with open(token_path, 'w') as token:
#             token.write(creds.to_json())
#     service = build('gmail', 'v1', credentials=creds)
#     user_info = service.users().getProfile(userId='me').execute()
#     print("Authenticated email:", user_info['emailAddress'])
#     return service

def get_gmail_service(user_id):
    token_data = read_creds(user_id)
    expiry_value = token_data['expiry']
    # Convert bigint -> ISO 8601 string (what google expects)
    if isinstance(expiry_value, (int, float)):
        expiry_value = datetime.fromtimestamp(expiry_value, tz=timezone.utc).isoformat().replace("+00:00", "Z")
    user_creds = {
    "token": token_data['access_token'],
    "refresh_token": token_data['refresh_token'],
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": client_id,
    "client_secret": client_secret,
    "scopes": ["https://www.googleapis.com/auth/gmail.readonly"],
    "expiry": expiry_value
    }
    creds = Credentials.from_authorized_user_info(user_creds, scopes=SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        write_creds(token_data['connected_email'], creds.token, creds.refresh_token, creds.expiry, user_id)
    service = build('gmail', 'v1', credentials=creds)
    return service
    

def connect_gmail(user_id):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    print("Received user_id:", user_id)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    creds_path = os.path.join(BASE_DIR, "credentials.json")
    print("Starting OAuth flow...")
    # redirect_url = "http://localhost:5173/oauth2callback"

    flow = InstalledAppFlow.from_client_secrets_file(
        creds_path,
        scopes=SCOPES
    )
    creds = flow.run_local_server(
        host="localhost",
        port=8080,
        open_browser=True
    )
    print("OAuth complete. Got creds.")

    service = build("gmail", "v1", credentials=creds)
    print("Built Gmail service.")

    user_info = service.users().getProfile(userId="me").execute()
    print("Got user info:", user_info)

    email = user_info.get("emailAddress")
    access_token = creds.token
    refresh_token = creds.refresh_token
    expiry = creds.expiry

    print("Writing creds to DB...")
    write_creds(email, access_token, refresh_token, expiry, user_id)
    print("✅ Done!")


def get_new_email_ids(current_service, last_timestamp):
    if last_timestamp is None:
        last_timestamp = 0
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

def _get_header_value(headers, name):
    for h in headers:
        if h.get("name") == name:
            return h.get("value")
    return None

def get_body(message):
    """Extracts all visible text from a Gmail message, preserving link text and nested elements."""

    def extract_text_from_html(html_content):
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove invisible elements
        for tag in soup(["script", "style", "noscript", "meta", "head"]):
            tag.decompose()

        # Insert newlines before block-level elements for readability
        for block in soup.find_all(["p", "div", "br", "tr", "table", "li"]):
            block.insert_before("\n")

        # Preserve the visible text from links, including nested tags
        for a in soup.find_all("a"):
            a.replace_with(a.get_text(" ", strip=True))

        text = soup.get_text(separator="\n", strip=True)
        return html.unescape(text)

    def extract_from_parts(parts):
        texts = []
        for part in parts:
            mime_type = part.get("mimeType", "")
            body = part.get("body", {})
            data = body.get("data")

            # Recurse into nested parts
            if "parts" in part:
                texts.append(extract_from_parts(part["parts"]))

            # Skip attachments
            if "attachmentId" in body:
                continue

            if data:
                decoded = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                if mime_type == "text/plain":
                    texts.append(decoded.strip())
                elif mime_type == "text/html":
                    texts.append(extract_text_from_html(decoded))

        return "\n".join(t for t in texts if t)

    payload = message.get("payload", {})
    parts = payload.get("parts")

    if parts:
        text = extract_from_parts(parts)
    else:
        # Single-part message
        body = payload.get("body", {}).get("data")
        mime_type = payload.get("mimeType", "")
        if body:
            decoded = base64.urlsafe_b64decode(body).decode("utf-8", errors="ignore")
            text = (
                extract_text_from_html(decoded)
                if mime_type == "text/html"
                else decoded.strip()
            )
        else:
            text = ""

    return text.strip()


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
        try:
            headers = current_message.get("payload", {}).get("headers", [])
            email_content[id]["ThreadId"] = current_message.get("threadId")
            email_content[id]["MessageId"] = _get_header_value(headers, "Message-ID")
            email_content[id]["InReplyTo"] = _get_header_value(headers, "In-Reply-To")
        except Exception:
            email_content[id]["ThreadId"] = None
            email_content[id]["MessageId"] = None
            email_content[id]["InReplyTo"] = None
    return email_content

def retrieve_gmails(user_id):
    service = get_gmail_service(user_id)
    timestamp = read_last_timestamp(user_id)
    ids_for_processing, latest_timestamp = get_new_email_ids(service, timestamp)
    print(f"Found {len(ids_for_processing)} new emails")
    content = get_content(ids_for_processing, service)
    return content, latest_timestamp

    
# This part is just for testing our function directly
if __name__ == '__main__':
    test = retrieve_gmails()
    with open("backend/emails.json", "w", encoding="utf-8") as f:
        json.dump(test, f, indent=4, ensure_ascii=False)
    print("Saved to backend/emails.json")
