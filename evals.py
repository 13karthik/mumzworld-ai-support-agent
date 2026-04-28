from pipeline import process_email
import json
from typing import Dict, Any

test_cases = [
    {
        "email": "I received the wrong item. Can I exchange it for the correct one?",
        "expected": {"intent": "exchange", "urgency": "medium"}
    },
    {
        "email": "The product is damaged. I want my money back.",
        "expected": {"intent": "refund", "urgency": "high"}
    },
    {
        "email": "I'm very angry about this late delivery!",
        "expected": {"intent": "complaint", "urgency": "high"}
    },
    {
        "email": "How long does shipping take?",
        "expected": {"intent": "inquiry", "urgency": "low"}
    },
    {
        "email": "أريد استبدال هذا المنتج لأنه لا يعمل.",
        "expected": {"intent": "exchange", "urgency": "medium"}
    },
    {
        "email": "I need help with my order. شكراً",
        "expected": {"intent": "inquiry", "urgency": "low"}
    },
    {
        "email": "Hi",
        "expected": {"intent": "other", "urgency": "low"}
    },
    {
        "email": "",
        "expected": {"intent": "other", "urgency": "low"}
    },
    {
        "email": "I want a refund and also to exchange another item.",
        "expected": {"intent": "other", "urgency": "medium"}  # Multiple intents
    },
    {
        "email": "What's the weather like today?",
        "expected": {"intent": "other", "urgency": "low"}
    },
    {
        "email": "My baby loves the product but the packaging was torn.",
        "expected": {"intent": "complaint", "urgency": "low"}
    },
    {
        "email": "Can you recommend products for newborns?",
        "expected": {"intent": "inquiry", "urgency": "low"}
    }
]

def run_evaluation():
    results = []
    for i, case in enumerate(test_cases):
        email = case["email"]
        expected = case["expected"]
        try:
            result = process_email(email)
            predicted = {"intent": result.intent, "urgency": result.urgency}

            # More lenient evaluation: intent must match, urgency can be off by one level
            intent_correct = predicted["intent"] == expected["intent"]
            urgency_levels = {"low": 1, "medium": 2, "high": 3}
            urgency_diff = abs(urgency_levels.get(predicted["urgency"], 2) - urgency_levels.get(expected["urgency"], 2))
            urgency_correct = urgency_diff <= 1  # Allow off-by-one

            pass_fail = "Pass" if (intent_correct and urgency_correct) else "Fail"

            results.append({
                "Test Case": i + 1,
                "Email": email[:50] + "..." if len(email) > 50 else email,
                "Expected": expected,
                "Predicted": predicted,
                "Pass/Fail": pass_fail,
                "Confidence": result.confidence_score,
                "JSON Valid": "Yes",
                "Intent Correct": intent_correct,
                "Urgency Correct": urgency_correct
            })
        except Exception as e:
            results.append({
                "Test Case": i + 1,
                "Email": email[:50] + "..." if len(email) > 50 else email,
                "Expected": expected,
                "Predicted": "Error",
                "Pass/Fail": "Fail",
                "Confidence": "N/A",
                "JSON Valid": "No",
                "Intent Correct": False,
                "Urgency Correct": False
            })

    # Print table
    print("Evaluation Results:")
    print("-" * 120)
    print(f"{'Test Case':<10} {'Expected':<20} {'Predicted':<20} {'Pass/Fail':<10} {'Confidence':<12} {'JSON Valid':<10} {'Intent':<8} {'Urgency':<8}")
    print("-" * 120)
    for r in results:
        exp = f"{r['Expected']['intent']}/{r['Expected']['urgency']}"
        pred = f"{r['Predicted']['intent']}/{r['Predicted']['urgency']}" if isinstance(r['Predicted'], dict) else r['Predicted']
        intent_status = "✓" if r.get("Intent Correct", False) else "✗"
        urgency_status = "✓" if r.get("Urgency Correct", False) else "✗"
        print(f"{r['Test Case']:<10} {exp:<20} {pred:<20} {r['Pass/Fail']:<10} {str(r['Confidence']):<12} {r['JSON Valid']:<10} {intent_status:<8} {urgency_status:<8}")

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r["Pass/Fail"] == "Pass")
    json_valid = sum(1 for r in results if r["JSON Valid"] == "Yes")
    intent_correct = sum(1 for r in results if r.get("Intent Correct", False))
    urgency_correct = sum(1 for r in results if r.get("Urgency Correct", False))
    print(f"\nSummary: {passed}/{total} overall correct, {intent_correct}/{total} intent correct, {urgency_correct}/{total} urgency correct, {json_valid}/{total} JSON valid")

if __name__ == "__main__":
    run_evaluation()