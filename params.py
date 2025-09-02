#The local ollama model to use:
model_name = "gemma3:1b-it-qat"

#The endpoint for the local ollama server:
ollama_endpoint = "http://localhost:11434/api/generate"

#States for the prompt:
states = ["Irrelevant", "Rejected", "Accepted", "Assessment Centre", "Interview", "Offer"]

#The email we want to classify:
email_content = "You have been invited to an interview for the Software Engineer position at TechCorp. Please let us know your availability."

#The improved prompt:
prompt = f"""
You are an expert email classifier. Your task is to classify the email content into one of the following categories. 
The first category is for emails that are not relevant to job applications. 
The other categories are for various stages of a job application process.

Valid categories: {states}
Your response must be a single word from the list and nothing else.

--- EMAIL CONTENT ---
{email_content}
---

CLASSIFICATION:
"""