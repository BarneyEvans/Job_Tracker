from database import add_to_tables
from extraction import extract_information

processed_emails = extract_information()
for email_id in processed_emails.keys():
    print(f"Adding {processed_emails[email_id]['company']} to table")
    add_to_tables(processed_emails[email_id])