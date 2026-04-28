import sys
import json
import logging
from datetime import datetime
from pipeline import process_email

# Set up logging
logging.basicConfig(
    filename='triage_log.jsonl',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def save_to_file(result, email):
    """Save triage result to JSON file"""
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "email": email,
        "result": result.model_dump()
    }

    # Save to JSONL file
    with open('triage_results.jsonl', 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    # Log the classification
    logging.info(f"Email triaged - Intent: {result.intent}, Urgency: {result.urgency}, Confidence: {result.confidence_score}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py 'customer email text'")
        print("Example: python main.py 'I want to return this product.'")
        return

    email = " ".join(sys.argv[1:])
    try:
        result = process_email(email)
        print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))

        # Save result and log
        save_to_file(result, email)

    except Exception as e:
        print(f"Error: {str(e)}")
        logging.error(f"Error processing email '{email}': {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()