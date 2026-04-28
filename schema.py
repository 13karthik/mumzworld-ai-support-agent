from pydantic import BaseModel, Field, validator
from typing import Literal

class TriageOutput(BaseModel):
    intent: Literal["refund", "exchange", "complaint", "inquiry", "other"] = Field(..., description="The intent of the email")
    urgency: Literal["low", "medium", "high"] = Field(..., description="The urgency level")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    reasoning: str = Field(..., description="Short explanation grounded in the input")
    suggested_reply_english: str = Field(..., description="Suggested reply in English")
    suggested_reply_arabic: str = Field(..., description="Suggested reply in Arabic")