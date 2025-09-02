#The local ollama model to use:
possible_models = ["gemma3:270m", "gemma3:270m-it-qat", "gemma3:1b", "gemma3:1b-it-qat", "gemma3:4b"]
model_name = possible_models[4]

#The endpoint for the local ollama server:
ollama_endpoint = "http://localhost:11434/api/generate"

#States for the prompt:
states = ["Irrelevant", "Not Sure", "Rejected", "Accepted", "Assessment Centre", "Online Test", "Interview", "Job Offer", "New Job Application"]

#The email we want to classify:
email_content = """Hi Barney, I want to sell you a potato peeler. It's the best on the market and will change your life! Best, Spud Seller. If you buy"""

#The prompt:
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