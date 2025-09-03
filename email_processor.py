import json
from datetime import datetime
from email_fetcher import (
    load_checkpoint,
    update_checkpoint,
    is_already_processed,
    fetch_emails_to_process,
    get_gmail_service
)
from classifier import classify_email, should_continue_processing

def mark_email_as_read(email_id):
    """Mark an email as read in Gmail"""
    service = get_gmail_service()
    try:
        service.users().messages().modify(
            userId='me',
            id=email_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        return True
    except Exception as e:
        print(f"Error marking email as read: {e}")
        return False

def save_classification_log(email_data, classification, confidence):
    """Save classification results for debugging/analysis"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "email_id": email_data['email_id'],
        "subject": email_data['subject'],
        "sender": email_data['sender_email'],
        "classification": classification,
        "confidence": confidence
    }
    
    # Append to log file
    with open('classification_log.json', 'a') as f:
        json.dump(log_entry, f)
        f.write('\n')

def process_emails_with_classification():
    """Main pipeline with classification"""
    checkpoint = load_checkpoint()
    emails = fetch_emails_to_process(checkpoint)
    
    print(f"\n{'='*60}")
    print(f"Processing {len(emails)} emails")
    print(f"{'='*60}\n")
    
    stats = {
        "total": len(emails),
        "irrelevant": 0,
        "job_related": 0,
        "errors": 0
    }
    
    for i, email in enumerate(emails, 1):
        print(f"\n[{i}/{len(emails)}] Processing email...")
        print(f"Subject: {email['subject']}")
        print(f"From: {email['sender_email']}")
        
        # PHASE 2: Classification
        try:
            classification, confidence = classify_email(
                email['subject'], 
                email['body']
            )
            
            print(f"Classification: {classification} (confidence: {confidence})")
            
            # Log the classification
            save_classification_log(email, classification, confidence)
            
            # Decision gate
            if not should_continue_processing(classification):
                print("→ Marking as irrelevant and skipping")
                stats["irrelevant"] += 1
                
                # Mark as read if it was unread
                if email['is_unread']:
                    mark_email_as_read(email['email_id'])
                
                # Update checkpoint and continue
                update_checkpoint(email['email_id'], email['date'])
                continue
            
            # Job-related email - will continue to Phase 3
            print(f"→ Job-related email detected: {classification}")
            stats["job_related"] += 1
            
            # TODO: Phase 3 - Information Extraction
            # For now, just update checkpoint
            update_checkpoint(email['email_id'], email['date'])
            
        except Exception as e:
            print(f"Error processing email {email['email_id']}: {e}")
            stats["errors"] += 1
            # Still update checkpoint to avoid reprocessing
            update_checkpoint(email['email_id'], email['date'])
        
        print("-" * 60)
    
    # Print summary
    print(f"\n{'='*60}")
    print("PROCESSING SUMMARY")
    print(f"{'='*60}")
    print(f"Total emails processed: {stats['total']}")
    print(f"Job-related: {stats['job_related']}")
    print(f"Irrelevant: {stats['irrelevant']}")
    print(f"Errors: {stats['errors']}")

if __name__ == '__main__':
    process_emails_with_classification()