from typing import TypedDict, Any

class AgentState(TypedDict):
    question: str
    schema: dict[str, Any]
    prompt: str | None
    raw_code: str | None
    extracted_code: str | None
    valid_code: bool | None
    result: Any | None
    explained_result: str | None
    authorized: bool | None
    rejection_reason: str | None
    request_received: bool | None
    request_classified: bool | None
    analysis_done: bool | None
    answered: bool | None
    attempts: int | None