from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime
from params import STAGES, SUBSTATES, get_upcoming_timings
from llm_call import send_request, format_response
import time

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase_client = create_client(url, key)


def new_email(data, application_id):
    response = (
        supabase_client.table("application_events")
            .insert(
                {
                    "event_date": data["date"], 
                    "application_id": application_id,
                    "email_text": data["content"],
                    "event_summary": data["subject"],
                }
            )
            .execute()
        )
    
def new_application(data, user_id=os.getenv('USER_ID')):
    response = (
        supabase_client.table("job_applications")
        .select("company, application_id")
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
                .execute()
            )
        elif (data["substate"] not in SUBSTATES or data["substate"] == "unsure"):
            response = (
                supabase_client.table("job_applications")
                .update({"latest_date": data["date"],
                        "stage": data["status"],
                        })
                .eq("company", data["company"])
                .execute()
            )
        elif (data["status"] not in STAGES or data["status"] == "unsure"):
            response = (
                supabase_client.table("job_applications")
                .update({"latest_date": data["date"],
                        "substate": data["substate"],
                        })
                .eq("company", data["company"])
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
                .execute()
            )
        index = companies.index(data["company"])
        return application_ids[index]
    else:
        response = (
            supabase_client.table("job_applications")
            .insert(
                {
                    "user": user_id, 
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

def new_calendar(data, application_id):
    if data["substate"] == "upcoming":
        prompt = get_upcoming_timings(data["content"])
        output = send_request(prompt, ollama=False)
        
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
        

def read_last_timestamp(user_id=os.getenv('USER_ID')):
    response = (
        supabase_client.table("user_email")
        .select("last_timestamp")
        .eq("user_id", user_id)
        .execute()
    )
    return response.data[0]["last_timestamp"]

def write_last_timestamp(timestamp, user_id=os.getenv('USER_ID')):
    response = (
            supabase_client.table("user_email")
            .update({"last_timestamp": timestamp,})
            .eq("user_id", user_id)
            .execute()
        )

def add_to_tables(data):
    application_id = new_application(data)
    new_email(data, application_id)
    new_calendar(data,application_id)

def add_user_to_table(data):
    response = (
            supabase_client.table("user_email")
            .insert(
                {
                    "last_timestamp": int(time.time() * 1000),
                    "connected_email": data["connected_email"],
                    "user_email": data["user_email"],
                    "user_id": data["user_id"],
                }
            )
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