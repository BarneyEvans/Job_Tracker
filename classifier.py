import requests
import json
from params import (
    OLLAMA_ENDPOINT, 
    CLASSIFICATION_MODEL, 
    JOB_STATES,
    MAX_CLASSIFICATION_RETRIES,
    CLASSIFICATION_TIMEOUT
)

def build_classification_prompt(email_subject, email_body):
    """Build the classification prompt for the model"""
    
    # Truncate body if too long (keep it under 2000 chars for faster processing)
    truncated_body = email_body[:2000] if len(email_body) > 2000 else email_body
    
    prompt = f"""You are an expert email classifier for job applications. 
Classify this email into EXACTLY ONE of these categories:
{', '.join(JOB_STATES)}

Rules:
- "Irrelevant": Not related to job applications (spam, newsletters, personal emails)
- "Applied": Confirmation that an application was received
- "Interview": Any interview invitation or scheduling
- "Assessment": Online tests, assessments, or assessment centres
- "Offer": Job offer or offer-related discussion
- "Rejected": Application rejected or position filled

Respond with ONLY the category word, nothing else.

EMAIL SUBJECT: {email_subject}
EMAIL BODY: {truncated_body}

CLASSIFICATION:"""
    
    return prompt

def classify_email(email_subject, email_body):
    """
    Classify an email using the Ollama model.
    Returns: (status, confidence)
    """
    prompt = build_classification_prompt(email_subject, email_body)
    
    for attempt in range(MAX_CLASSIFICATION_RETRIES):
        try:
            # Call Ollama
            response = requests.post(
                OLLAMA_ENDPOINT,
                json={
                    "model": CLASSIFICATION_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.1,  # Low temperature for consistency
                    "top_p": 0.9
                },
                timeout=CLASSIFICATION_TIMEOUT
            )
            
            if response.status_code != 200:
                print(f"Ollama error: {response.status_code}")
                continue
                
            result = response.json().get('response', '').strip()
            
            # Validate the response
            if result in JOB_STATES:
                return result, "high"
            
            # Try to fuzzy match if not exact
            result_lower = result.lower()
            for state in JOB_STATES:
                if state.lower() in result_lower:
                    return state, "medium"
            
            print(f"Invalid classification result: {result}")
            
        except requests.exceptions.Timeout:
            print(f"Classification timeout on attempt {attempt + 1}")
        except Exception as e:
            print(f"Classification error on attempt {attempt + 1}: {e}")
    
    # If all retries failed, default to Irrelevant with low confidence
    return "Irrelevant", "low"

def should_continue_processing(classification):
    """Determine if we should continue to extraction phase"""
    return classification != "Irrelevant"