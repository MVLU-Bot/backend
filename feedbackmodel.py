from pydantic import BaseModel
from typing import Optional

class FeedbackModel(BaseModel):
    question: str
    answer: str
    feedback: bool
    message: str
    context: Optional[str] = None
