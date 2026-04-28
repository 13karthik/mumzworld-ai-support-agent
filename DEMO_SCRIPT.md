# 3-Minute Loom Demo Script - Mumzworld AI Triage System

## Overview (30 seconds)
**Show**: README.md on screen

*Talking Points:*
- "This is an AI-powered email triage system for Mumzworld, an e-commerce platform for mothers"
- "It classifies customer support emails into intents like refund, exchange, complaint, or inquiry"
- "It handles multilingual input - English and Arabic - and generates bilingual responses"
- "Built with GPT-3.5-turbo for accuracy and reliability"

---

## Feature 1: CLI Demo - Refund Request (30 seconds)
**Show**: Terminal with command execution

*Commands to run:*
```bash
python main.py "I want a refund for this damaged product"
```

**Talking Points:**
- "Here's the CLI interface - you just pass an email as a string"
- "Notice the intent is correctly detected as 'refund'"
- "The urgency is properly set to 'high' for a damaged product"
- "Confidence score is strong at 0.8"
- "The system generates helpful replies in both English and Arabic"

---

## Feature 2: CLI Demo - Exchange Request (25 seconds)
**Show**: Terminal with command execution

*Commands to run:*
```bash
python main.py "I received the wrong size, can I exchange it?"
```

**Talking Points:**
- "Here's an exchange request"
- "The system correctly identifies it as 'exchange' intent"
- "Notice the post-processing rules detect the 'wrong size' keyword"
- "Confidence score above 0.7 shows strong classification"
- "Both English and Arabic replies are culturally appropriate"

---

## Feature 3: Web UI - Streamlit Demo (1 minute)
**Show**: Browser with Streamlit app running at localhost:8501

*Steps:*
1. Show the clean, intuitive interface
2. Enter a test email: "Hi, I'm very angry about my late delivery"
3. Click "Classify Email"
4. Show the structured JSON output

**Talking Points:**
- "We also built a Streamlit web UI for interactive testing"
- "The interface is simple and user-friendly"
- "You can paste any customer email and get instant classification"
- "The output includes intent, urgency, confidence, and bilingual replies"
- "Perfect for demonstrations or manual testing"

---

## Feature 4: Evaluation Results (30 seconds)
**Show**: README.md - Evaluation Results section

*Talking Points:*
- "We evaluated the system on 12 diverse test cases"
- "Achieved 92% overall accuracy and 100% JSON validity"
- "100% accuracy on intent classification"
- "92% accuracy on urgency classification with lenient evaluation"
- "The system handles edge cases like mixed-language input and vague emails"

---

## Bonus Features (15 seconds)
**Show**: Key files in the project

*Talking Points:*
- "The system includes automatic logging to triage_results.jsonl"
- "All outputs are validated using Pydantic schemas"
- "Low API costs - about $0.002 per request"
- "Production-ready architecture with retry mechanisms and error handling"

---

## Closing (5 seconds)
**Show**: README.md - Top section

*Talking Points:*
- "This is a complete, production-quality solution"
- "Ready to handle real customer support emails"
- "All code is open-source and available on GitHub"

---

## Total Time: ~3 minutes

### Tips for Recording:
1. **Screen Resolution**: Set to 1920x1080 for clarity
2. **Font Size**: Increase terminal font for readability
3. **Cursor**: Move slowly to guide viewers
4. **Pauseflow**: Pause for 1-2 seconds after each result for viewers to read
5. **Audio**: Speak clearly and at a moderate pace
6. **Background**: Quiet environment, no distractions
7. **Camera**: Optional - you can do screen-only for technical demos

### Files to Have Open:
- [ ] Terminal (for CLI demos)
- [ ] Browser with Streamlit app running
- [ ] README.md in editor
- [ ] Project file structure visible
