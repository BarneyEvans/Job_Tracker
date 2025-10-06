from database import add_to_tables, add_user_to_table, write_last_timestamp, delete_application_records
from extraction import extract_information



def check_updates(user_id):
    processed_emails, latest_timestamp = extract_information(user_id)
    print("abyeys")
    print(processed_emails)
    for email_id in processed_emails.keys():
        print(f"Adding {processed_emails[email_id]['company']} to table")
        add_to_tables(processed_emails[email_id], user_id)
    write_last_timestamp(latest_timestamp, user_id)

def sign_up(email):
    None

def connect_email(payload):
    add_user_to_table(payload)
    check_updates(payload["user_id"])


def remove_application(application_id, user_id):
    return delete_application_records(application_id, user_id)
