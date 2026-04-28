import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if api_key:
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )
else:
    client = None

def call_llm(system_prompt: str, user_prompt: str, model: str = "openai/gpt-3.5-turbo", temperature: float = 0.1) -> str:
    if not api_key:
        # Mock response for testing
        return '''{
  "intent": "other",
  "urgency": "low",
  "confidence_score": 0.5,
  "reasoning": "Mock response - no API key configured",
  "suggested_reply_english": "Hello! How can we help you today?",
  "suggested_reply_arabic": "مرحباً! كيف يمكننا مساعدتك اليوم؟"
}'''
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=1500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"LLM call failed: {str(e)}")