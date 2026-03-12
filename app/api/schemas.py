from pydantic import BaseModel
from typing import Any

class QuestionRequest(BaseModel):
    question: str

class AgentResponse(BaseModel):
    result: Any
    valid_code: bool
    error: str | None = None
    attempts: int = 0
    explanation: str | None = None

class ErrorResponse(BaseModel):
    error: str
    details: dict[str, Any] | None = None