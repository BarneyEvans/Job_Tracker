from extraction import information_extraction
from params import EXTRACTION_STATES, generate_checking_prompt
from extraction import get_result
import pandas as pd
import json

def load_job_tracker(file_path='job_tracker.csv'):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        copy = EXTRACTION_STATES.copy()
        copy.append("Classification")
        copy.append("Sender_Email")
        df = pd.DataFrame(columns=copy)
        df.to_csv(file_path, index=False)
        return df
    

def find_candidate_jobs(all_jobs_df):
    candidate_jobs = all_jobs_df[all_jobs_df['Classification'].str.upper() != 'REJECTED']
    return candidate_jobs

def check_current_jobs():
    df = load_job_tracker()
    candidate_jobs = find_candidate_jobs(df)
    emails = information_extraction()

    for id in emails:
        address = emails[id].get("Sender_Email", "UNKNOWN").strip()
        company = emails[id].get("Company Name", "UNKNOWN").strip()
        job_title = emails[id].get("Job Title", "UNKNOWN").strip()
        current_job_details = f"Company: {company}, Sender_Email: {address}, Job Title: {job_title}"
        mega_string = f""
        for original_index in candidate_jobs.index:
            job_row = candidate_jobs.loc[original_index]
            existing_company = job_row['Company Name']
            existing_email = job_row['Sender_Email'] 
            existing_job_title = job_row['Job Title']
            string = f"Company: {existing_company}, Sender_Email: {existing_email}, Job Title: {existing_job_title}, Row Number: {original_index} |"
            mega_string += string + "\n"

        prompt = generate_checking_prompt(current_job_details, mega_string)
        result = get_result(prompt)
        emails[id]["Duplicate_Check"] = result.strip()
    
    return emails

def update_processed_ids(new_ids):
    with open("checkpoint.json", "r") as f:
        checkpoint_data = json.load(f)

    processed_ids = set(checkpoint_data['processed_ids'])
    processed_ids.update(set(new_ids))
    checkpoint_data['processed_ids'] = list(processed_ids)

    with open("checkpoint.json", "w") as f:
        json.dump(checkpoint_data, f)

def update_list():
    emails = check_current_jobs()
    df = load_job_tracker()
    copy = EXTRACTION_STATES.copy()
    copy.append("Classification")
    copy.append("Sender_Email")
    id_list = []
    for id in emails:
        value = emails[id]["Duplicate_Check"]
        id_list.append(id)
        if value.lower() == "none":
            df.loc[len(df)] = [emails[id]["Company Name"] ,emails[id]["Job Title"],emails[id]["Location"],emails[id]["Salary"],emails[id]["Required Skills"], emails[id]["Classification"], emails[id]["Sender_Email"]]
        else:
            for field in copy:
                if emails[id].get(field, "UNKNOWN") != "UNKNOWN":
                    df.loc[int(value), field] = emails[id][field]
    df.to_csv('job_tracker.csv', index=False)
    update_processed_ids(id_list)
        
        


if __name__ == '__main__':
    update_list()