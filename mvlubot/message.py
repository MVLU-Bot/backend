from pydantic import BaseModel, Field
from typing import  Literal, Optional, List

class Message(BaseModel):
    role: Literal["MVLUBOT", "USER"] = "USER"
    message: str = Field("", title="User input message")
    history: Optional[List["Message"]] = []