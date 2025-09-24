POSSIBLE_MODELS = ["gemma3:270m", "gemma3:270m-it-qat", "gemma3:1b", "gemma3:1b-it-qat", "gemma3:4b", "deepseek-r1:7b"]
MODEL_NAME = POSSIBLE_MODELS[5]

#The endpoint for the local ollama server:
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"

#States for the prompt:
STATES = ["IRRELEVANT", "UNSURE", "REJECTED", "ACCEPTED", "ASSESSMENT", "INTERVIEW", "JOB OFFER", "APPLIED", "ACTION REQUIRED"]

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

    There are 4 key pieces of information that you are required to gather. These are as follows:

    company_name: This is the name of the company that the email is coming from. (e.g. Samsung, Meta, BlackRock)
    job_name: This is the name of the job that has been applied for and the email is referencing. (e.g. Software Engineer, Data Scientist, Quant Analyst)
    status: This is the stage of the job application. Please select the most suitable item in this list {STATES}.
    job_position: This is the position of the job. Please select the most suitable item in this list {POSITIONS}.

    The following is the email content:
    --- EMAIL CONTENT ---
    Subject: {email_subject}
    Body: {email_body}
    ---

    Please return your response as a json in the following format:
    {{
        "company": company_name,
        "job_title": job_name,
        "status": status,
        "position": job_position
    }}

    Please think through step by step.
    """
    return prompt