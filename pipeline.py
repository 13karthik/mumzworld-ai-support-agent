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
            data = json.loads(raw_response)
            triage = TriageOutput(**data)

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
    """Apply deterministic rules to improve accuracy."""
    text = email.lower()

    refund_keywords = ["refund", "money back", "return my money", "استرداد", "استرجاع"]
    exchange_keywords = ["exchange", "replace", "wrong size", "wrong item", "استبدال", "تبديل"]
    inquiry_keywords = [
        "how long",
        "can you",
        "help with my order",
        "need help with my order",
        "recommend",
        "where is my order",
        "shipping",
        "شحن",
        "مساعدة",
    ]

    has_refund = any(keyword in text for keyword in refund_keywords)
    has_exchange = any(keyword in text for keyword in exchange_keywords)

    # ---- Intent overrides ----
    if has_refund and has_exchange:
        result.intent = "other"
        result.urgency = "medium"
        result.confidence_score = min(result.confidence_score, 0.45)
    elif has_refund:
        result.intent = "refund"
    elif has_exchange:
        result.intent = "exchange"
    elif result.intent == "other" and any(keyword in text for keyword in inquiry_keywords):
        result.intent = "inquiry"

    # ---- Urgency rules ----
    high_urgency_keywords = [
        "angry",
        "unacceptable",
        "immediately",
        "asap",
        "frustrated",
        "غاضب",
        "مستاء",
    ]
    medium_urgency_keywords = [
        "damaged",
        "broken",
        "not working",
        "late",
        "تالف",
        "مكسور",
        "متأخر",
    ]

    if any(keyword in text for keyword in high_urgency_keywords):
        result.urgency = "high"
    elif any(keyword in text for keyword in medium_urgency_keywords):
        if result.urgency == "low":
            result.urgency = "medium"

    # ---- Confidence guardrails ----
    if result.intent == "other":
        result.confidence_score = min(result.confidence_score, 0.5)
    else:
        result.confidence_score = max(result.confidence_score, 0.7)

    # Never output 0.0 for clear non-empty intents.
    if result.intent != "other" and result.confidence_score == 0.0 and email.strip():
        result.confidence_score = 0.7

    result.confidence_score = min(result.confidence_score, 0.95)

    return result
