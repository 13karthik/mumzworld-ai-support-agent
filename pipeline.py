from schema import TriageOutput
from prompts import system_prompt, get_user_prompt
from llm import call_llm
import json
import logging

logging.basicConfig(level=logging.INFO)

def process_email(email: str, max_retries: int = 2) -> TriageOutput:
    user_prompt = get_user_prompt(email)
    for attempt in range(max_retries + 1):
        try:
            raw_response = call_llm(system_prompt, user_prompt)
            logging.info(f"Attempt {attempt + 1}: Raw response: {raw_response}")
            # Try to parse JSON
            data = json.loads(raw_response)
            triage = TriageOutput(**data)

            # Apply deterministic post-processing rules
            triage = apply_post_processing_rules(email, triage)

            return triage
        except json.JSONDecodeError as e:
            logging.warning(f"JSON decode error on attempt {attempt + 1}: {e}")
            if attempt == max_retries:
                raise ValueError(f"Invalid JSON response after {max_retries + 1} attempts")
        except Exception as e:
            logging.warning(f"Validation error on attempt {attempt + 1}: {e}")
            if attempt == max_retries:
                raise e
    raise ValueError("Failed to get valid response after retries")

def apply_post_processing_rules(email: str, result: TriageOutput) -> TriageOutput:
    """Apply deterministic rules to improve accuracy"""
    text = email.lower()

    # ---- Intent overrides ----
    if any(k in text for k in ["refund", "money back", "return my money", "استرداد", "استرجاع"]):
        result.intent = "refund"
    elif any(k in text for k in ["exchange", "replace", "wrong size", "wrong item", "استبدال", "تبديل"]):
        result.intent = "exchange"

    # ---- Urgency rules ----
    if any(k in text for k in ["angry", "unacceptable", "immediately", "asap", "frustrated", "غاضب", "مستاء"]):
        result.urgency = "high"
    elif any(k in text for k in ["damaged", "broken", "not working", "late", "تالف", "مكسور", "متأخر"]):
        if result.urgency == "low":  # don't downgrade from high to medium
            result.urgency = "medium"

    # ---- Confidence guardrails ----
    if result.intent == "other":
        result.confidence_score = min(result.confidence_score, 0.5)
    else:
        result.confidence_score = max(result.confidence_score, 0.7)

    # Fix confidence bug - never output 0.0 unless truly empty
    if result.confidence_score == 0.0 and email.strip():
        result.confidence_score = 0.7

    # Cap confidence to avoid unrealistic 1.0
    result.confidence_score = min(result.confidence_score, 0.95)

    return result