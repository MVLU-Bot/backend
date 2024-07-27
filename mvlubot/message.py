from pydantic import BaseModel, Field
from typing import  Literal

class Message(BaseModel):
    role: Literal["MVLUBOT", "USER"] = "USER"
    message: str = Field("", title="User input message")