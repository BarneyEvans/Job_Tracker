POSSIBLE_MODELS = ["gemma3:270m", "gemma3:270m-it-qat", "gemma3:1b", "gemma3:1b-it-qat", "gemma3:4b", "deepseek-r1:7b"]
MODEL_NAME = POSSIBLE_MODELS[5]

#The endpoint for the local ollama server:
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"

#States for the prompt:
STAGES = ["irrelevant", "unsure","awaiting_response", "applied", "assessment", "interview"]

SUBSTATES = ["rejected", "accepted", "completed", "awaiting_response", "applied", "upcoming", "deadline"]

EXTRACTION_STATES = ["Company Name", "Job Title", "Location", "Salary", "Required Skills"]

POSITIONS = ["FULL_TIME", "PART_TIME", "INTERN", "CONTINGENCY"]

#The prompt:
def generate_classification_prompt(email_s, email_b):
    prompt = f"""
    You are an expert email classifier. Your task is to classify the email content into one of the following categories. 
    The first category is for emails that are not relevant to job applications. 
    The second category (UNSURE) is for emails that are job related but it's unclear what stage of the application process they pertain to.
    The other categories are for various stages of a job application process.

    Valid categories: {STATES}
    Your response must be a single category from the list and nothing more, only the category.

    --- EMAIL CONTENT ---
    Subject: {email_s}
    Body: {email_b}
    ---

    CLASSIFICATION:
    """

    return prompt

def generate_single_extraction_prompt(email_subject, email_body, field_to_extract):
    prompt = f"""
    You are a highly specialized information extraction tool. Your single task is to extract the "{field_to_extract}" from the email content below.

    Follow these rules precisely:
    1.  Only respond with the extracted information.
    2.  If you cannot find the "{field_to_extract}", you MUST respond with the single word "UNKNOWN".
    3.  Do not add any explanation, conversation, or extra text.

    --- EMAIL CONTENT ---
    Subject: {email_subject}
    Body: {email_body}
    ---
    """
    return prompt


def generate_checking_prompt(new_job_details, existing_jobs_list_as_string):
    prompt = f"""
    You are a highly intelligent duplicate detection system for a job application tracker. Your task is to determine if the "New Application" below is a duplicate of any of the "Existing Applications".

    --- RULES ---
    1.  A duplicate means it is for the same role at the same company. The job title can be a variation (e.g., "Software Engineer" matches "SWE" or "Junior Software Engineer").
    2.  If you find a clear duplicate, you MUST respond with only the Row Number of the matching application in the format "[Number]".
    3.  If there are no clear duplicates, you MUST respond with the single word "NONE".
    4.  Do not provide any explanation, reasoning, or extra text. Your entire response must be either "[Number]" or "NONE".

    --- EXISTING APPLICATIONS ---
    {existing_jobs_list_as_string}

    --- NEW APPLICATION ---
    {new_job_details}

    --- ANALYSIS ---
    """
    return prompt

def data_extraction_prompt(email_subject, email_body):
    prompt = f"""
    You are a highly specialized information extraction agent, tasked to extract the relevant information from an email.

    There are 5 key pieces of information that you are required to gather. These are as follows:

    company_name: This is the name of the company that the email is coming from. (e.g. Samsung, Meta, BlackRock)
    job_name: This is the name of the job that has been applied for and the email is referencing. (e.g. Software Engineer, Data Scientist, Quant Analyst)
    status: This is the stage of the job application. Please select the most suitable item from this list {STAGES}. (e.g. "Please schedule a meeting time" is "action_required"). Only use "irrelevant if the email has no possiblibility of filing under any other item in the list.
    substate: This is the outcome from the user so far. Please select the most suitable item from this list {SUBSTATES}. (e.g. "Unfortunately we have gone with other candidates" would be "rejected")
    job_position: This is the position of the job. Please select the most suitable item from this list {POSITIONS}.

    To understand the stages for 'status' please use the following information:
        applied: Can have only substates 'applied' or 'rejected'.
        awaiting_response: Can have only substates 'awaiting_response', 'completed' or 'rejected'.
        assessment: Can have substates only 'upcoming', 'completed' or 'rejected', "deadline.
        interview: Can have substates only 'upcoming', 'completed' or 'rejected'
    
    To understand the options for 'substates' please use the following information:
        applied: This is used when the candidate has only applied for a job and the email is an acknowledgment of the application. (e.g. Thank you for applying to BlackRock)
        rejected: This is used when the candidate has been rejected from the job. (e.g. Unfortunately we have decided to move forward with other candidates)
        accepted: This is when the candidate has been accepted for the job. (e.g. We would like to offer you a job opportunity at Meta)
        completed: This is when the candidate has completed a task and the email is an acknowledgment of completion. (e.g. Thank you for completing the coding assessment)
        awaiting_response: This is when the candidate must respond to the email as requested by the email. (e.g. Please select interview times)
        upcoming: This is when an interview or assessment has been scheduled and the email is a confirmation of the timings. (e.g. Your interview has been scheduled for Tuesday the 25th of February 2026)
        deadline: This is when an assessment has a deadline to be completed by. (e.g. Please complete this assessment within 7 days)

    The following is the email content:
    --- EMAIL CONTENT ---
    Subject: {email_subject}
    Body: {email_body}
    ---

    If 'status' is irrelevant, please return nothing (no characters), otherwise, please return your response as a json in the following format:
    {{
        "company": company_name,
        "job_title": job_name,
        "status": status,
        "substate": substate,
        "position": job_position
    }}

    Please think this through step by step.
    """
    return prompt