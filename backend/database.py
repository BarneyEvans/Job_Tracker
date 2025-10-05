from supabase import create_client, Client, ClientOptions
import os
from dotenv import load_dotenv
from datetime import datetime
from params import STAGES, SUBSTATES, get_upcoming_timings
from llm_call import send_request, format_response
import time

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase_client: Client = create_client(url, key)

THREADING_ENABLED = True

def find_application_by_thread(thread_id):
    if not THREADING_ENABLED or not thread_id:
        return None
    try:
        resp = (
            supabase_client.table("application_events")
            .select("application_id")
            .eq("gmail_thread_id", thread_id)
            .limit(1)
            .execute()
        )
        if resp.data:
            return resp.data[0]["application_id"]
    except Exception:
        return None
    return None

def find_application_by_in_reply_to(in_reply_to):
    if not THREADING_ENABLED or not in_reply_to:
        return None
    try:
        resp = (
            supabase_client.table("application_events")
            .select("application_id")
            .eq("gmail_message_id", in_reply_to)
            .limit(1)
            .execute()
        )
        if resp.data:
            return resp.data[0]["application_id"]
    except Exception:
        return None
    return None

def event_exists_by_message_id(message_id):
    if not THREADING_ENABLED or not message_id:
        return False
    try:
        resp = (
            supabase_client.table("application_events")
            .select("gmail_message_id")
            .eq("gmail_message_id", message_id)
            .limit(1)
            .execute()
        )
        return bool(resp.data)
    except Exception:
        return False

def update_existing_application(application_id, data, user_id):
    if (data["status"] not in STAGES or data["status"] == "unsure") and (data["substate"] not in SUBSTATES or data["substate"] == "unsure"):
        _ = (
            supabase_client.table("job_applications")
            .update({"latest_date": data["date"]})
            .eq("application_id", application_id)
            .eq("user_id", user_id)
            .execute()
        )
    elif (data["substate"] not in SUBSTATES or data["substate"] == "unsure"):
        _ = (
            supabase_client.table("job_applications")
            .update({"latest_date": data["date"], "stage": data["status"]})
            .eq("application_id", application_id)
            .eq("user_id", user_id)
            .execute()
        )
    elif (data["status"] not in STAGES or data["status"] == "unsure"):
        _ = (
            supabase_client.table("job_applications")
            .update({"latest_date": data["date"], "substate": data["substate"]})
            .eq("application_id", application_id)
            .eq("user_id", user_id)
            .execute()
        )
    else:
        _ = (
            supabase_client.table("job_applications")
            .update({
                "latest_date": data["date"],
                "stage": data["status"],
                "substate": data["substate"],
            })
            .eq("application_id", application_id)
            .eq("user_id", user_id)
            .execute()
        )
    return application_id

def resolve_application_id(data, user_id):
    thread_id = data.get("thread_id")
    in_reply_to = data.get("in_reply_to")
    app_id = find_application_by_thread(thread_id)
    if app_id is None:
        app_id = find_application_by_in_reply_to(in_reply_to)
    if app_id is not None:
        update_existing_application(app_id, data, user_id)
        return app_id
    return new_application(data, user_id)

def new_email(data, application_id, user_id):
    if THREADING_ENABLED and event_exists_by_message_id(data.get("message_id")):
        return
    event = {
        "event_date": data["date"],
        "application_id": application_id,
        "email_text": data["content"],
        "event_summary": data["subject"],
    }
    if THREADING_ENABLED:
        if data.get("thread_id") is not None:
            event["gmail_thread_id"] = data.get("thread_id")
        if data.get("message_id") is not None:
            event["gmail_message_id"] = data.get("message_id")
        if data.get("in_reply_to") is not None:
            event["in_reply_to"] = data.get("in_reply_to")
    try:
        _ = (
            supabase_client.table("application_events")
            .insert(event)
            .execute()
        )
    except Exception:
        fallback_event = {
            "event_date": data["date"],
            "application_id": application_id,
            "email_text": data["content"],
            "event_summary": data["subject"],
        }
        _ = (
            supabase_client.table("application_events")
            .insert(fallback_event)
            .execute()
        )
    
def new_application(data, user_id):
    response = (
        supabase_client.table("job_applications")
        .select("company, application_id")
        .eq("user_id", user_id)
        .execute()
    )

    companies = [row["company"] for row in response.data]
    application_ids = [row["application_id"] for row in response.data]
    if data["company"] in companies:
        if (data["status"] not in STAGES or data["status"] == "unsure") and (data["substate"] not in SUBSTATES or data["substate"] == "unsure"):
            response = (
                supabase_client.table("job_applications")
                .update({"latest_date": data["date"],})
                .eq("company", data["company"])
                .eq("user_id", user_id)
                .execute()
            )
        elif (data["substate"] not in SUBSTATES or data["substate"] == "unsure"):
            response = (
                supabase_client.table("job_applications")
                .update({"latest_date": data["date"],
                        "stage": data["status"],
                        })
                .eq("company", data["company"])
                .eq("user_id", user_id)
                .execute()
            )
        elif (data["status"] not in STAGES or data["status"] == "unsure"):
            response = (
                supabase_client.table("job_applications")
                .update({"latest_date": data["date"],
                        "substate": data["substate"],
                        })
                .eq("company", data["company"])
                .eq("user_id", user_id)
                .execute()
            )
        else:
            response = (
                supabase_client.table("job_applications")
                .update({"latest_date": data["date"],
                        "stage": data["status"],
                        "substate": data["substate"],
                        })
                .eq("company", data["company"])
                .eq("user_id", user_id)
                .execute()
            )
        index = companies.index(data["company"])
        return application_ids[index]
    else:
        response = (
            supabase_client.table("job_applications")
            .insert(
                {
                    "user_id": user_id,
                    "latest_date": data["date"],
                    "company": data["company"],
                    "job_title": data["job_title"],
                    "stage": data["status"],
                    "substate": data["substate"],
                    "position": data["position"],
                    "email_address": data["sender_email"]
                }
            )
            .execute()
        )

        application_id = response.data[0]["application_id"]
        return application_id

def new_calendar(data, application_id, user_id):
    if data["substate"] == "upcoming":
        prompt = get_upcoming_timings(data["content"])
        output = send_request(prompt, ollama=False)
        try: 
            out_json = format_response(output)
            parsed_email = eval(out_json)
            if str(parsed_email["duration"]) == "-1":
                response = (
                    supabase_client.table("calendar")
                    .insert(
                        {
                            "application_id": application_id, 
                            "date": parsed_email["upcoming_date"],
                            "time": parsed_email["time"],
                        }
                    )
                    .execute()
                )
            else:
                response = (
                    supabase_client.table("calendar")
                    .insert(
                        {
                            "application_id": application_id, 
                            "date": parsed_email["upcoming_date"],
                            "time": parsed_email["time"],
                            "duration": parsed_email["duration"],
                        }
                    )
                    .execute()
                )
        except:
            None
        

def read_last_timestamp(user_id):
    #user_id = os.getenv("USER_ID")  # hardcoded for testing
    response = (
        supabase_client.table("user_email")
        .select("last_timestamp")
        .eq("user_id", user_id)
        .execute()
    )
    if not response.data or len(response.data) == 0:
        return None  # or some default value

    return response.data[0]["last_timestamp"]

def write_last_timestamp(timestamp, user_id):
    response = (
            supabase_client.table("user_email")
            .update({"last_timestamp": timestamp,})
            .eq("user_id", user_id)
            .execute()
        )

def add_to_tables(data, user_id):
    application_id = resolve_application_id(data, user_id)
    new_email(data, application_id, user_id)
    new_calendar(data, application_id, user_id)


def delete_application_records(application_id, user_id):
    """Hard delete an application and all associated records."""
    try:
        existing = (
            supabase_client.table("job_applications")
            .select("application_id")
            .eq("application_id", application_id)
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )
    except Exception:
        return False

    if not existing.data:
        return False

    try:
        supabase_client.table("application_events").delete().eq("application_id", application_id).execute()
        supabase_client.table("calendar").delete().eq("application_id", application_id).execute()
        supabase_client.table("job_applications").delete().eq("application_id", application_id).eq("user_id", user_id).execute()
    except Exception:
        return False

    return True

def add_user_to_table(data, user_id):
    response = (
            supabase_client.table("user_email")
            .insert(
                {
                    "last_timestamp": int(time.time() * 1000),
                    "connected_email": data["connected_email"],
                    "user_email": data["user_email"],
                }
            )
            .eq("user_id", user_id)
            .execute()
        )

if __name__ == '__main__':
    dt = "Wed, 24 Sep 2025 10:44:56 +0000"
    data = {
        "subject": "Fw: Your Application to Gooning Group",
        "company": "Gooning Group",
        "job_title": "Junior Gooning Engineer",
        "status": "applied",
        "substate": "rejected",
        "position": "FULL_TIME",
        "date": datetime.strptime(dt, "%a, %d %b %Y %H:%M:%S %z").isoformat(),
        "sender_email": "jeremy.ockenden@goon.co.uk",
        "content": "Barney Likes Men"
    }
    add_to_tables(data)
