POSSIBLE_MODELS = ["gemma3:270m", "gemma3:270m-it-qat", "gemma3:1b", "gemma3:1b-it-qat", "gemma3:4b", "deepseek-r1:7b"]
MODEL_NAME = POSSIBLE_MODELS[5]

#The endpoint for the local ollama server:
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"

#States for the prompt:
STATES = ["IRRELEVANT", "UNSURE", "REJECTED", "ACCEPTED", "ONLINE TEST", "INTERVIEW", "JOB OFFER", "NEW JOB APPLICATION"]

#The prompt:
def generate_classification_prompt(email_s, email_b):
    prompt = f"""
    You are an expert email classifier. Your task is to classify the email content into one of the following categories. 
    The first category is for emails that are not relevant to job applications. 
    The second category is for emails that are job related but it's unclear what stage of the application process they pertain to.
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

def generate_info_extractor_prompt(email_s, email_b):
    prompt = f"""
    You are an expert information extractor. From the email below, extract the following fields: Company, JobTitle, Location, Salary.

    Rules:
    - Respond with each field on a new line, in "Key: Value" format.
    - If a field is not mentioned in the email, use "UNKNOWN" as its value.
    - Do not add any other text, explanation, or conversation.

    --- EMAIL CONTENT ---
    Subject: {email_s}
    Body: {email_b}
    ---

    EXTRACTION:
    """
    return prompt


    
