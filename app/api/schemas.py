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
    

class EvalRequest(BaseModel):
    test_cases: list[str] | None = None

class EvalResultItem(BaseModel):
    question: str
    result: str | None
    valid_code: bool
    error: str | None
    repair_attempts: int
    needs_clarification: bool

class EvalResponse(BaseModel):
    results: list[EvalResultItem]
    metrics: dict