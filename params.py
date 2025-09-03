# GENERAL PARAMS - PROBS DON'T CHANGE THESE
FALLBACK_EMAIL_COUNT = 2

# Model settings
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
CLASSIFICATION_MODEL = "gemma2:4b"  # Updated from gemma3 to gemma2 for consistency

# Legacy model settings (kept for backward compatibility)
possible_models = ["gemma3:270m", "gemma3:270m-it-qat", "gemma3:1b", "gemma3:1b-it-qat", "gemma3:4b", "deepseek-r1:7b"]
model_name = possible_models[4]
ollama_endpoint = "http://localhost:11434/api/generate"

# Classification categories
JOB_STATES = [
    "Irrelevant",      # Not job-related
    "Applied",         # Application confirmation
    "Interview",       # Interview invitation/scheduling
    "Assessment",      # Online test/assessment center
    "Offer",          # Job offer received
    "Rejected"        # Application rejected
]

# Legacy states (kept for backward compatibility)
states = ["IRRELEVANT", "UNSURE", "REJECTED", "ASSESSMENT CENTRE", "ONLINE TEST", "INTERVIEW", "JOB OFFER", "NEW JOB APPLICATION"]

# Retry settings
MAX_CLASSIFICATION_RETRIES = 3
CLASSIFICATION_TIMEOUT = 30  # seconds

# Legacy email content and prompt (kept for backward compatibility)
email_content = """Hi Barney, you have now been invited for an in person, all day activity of tasks to test your ability for META"""

prompt = f"""
You are an expert email classifier. Your task is to classify the email content into one of the following categories. 
The first category is for emails that are not relevant to job applications. 
The second category is for emails that are job related but it's unclear what stage of the application process they pertain to.
The other categories are for various stages of a job application process.

Valid categories: {states}
Your response must be a single category from the list and nothing else.

--- EMAIL CONTENT ---
{email_content}
---

CLASSIFICATION:
"""