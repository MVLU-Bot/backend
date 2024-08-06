from pydantic import BaseModel
from typing import Literal, Optional, List

class FeedbackModel(BaseModel):
    question: str
    answer: str
    feedback: bool
    message: str
