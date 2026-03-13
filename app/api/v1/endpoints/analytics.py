from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path

from app.graph.graph_builder import run_agent
from app.api.schemas import QuestionRequest, AgentResponse

router = APIRouter()

TEMPLATE_PATH = Path("app/web/index.html")

@router.get("/", response_class=HTMLResponse)
def home():
    if not TEMPLATE_PATH.exists():
        return f"<h3>Template file not found at {TEMPLATE_PATH}</h3>"
    return TEMPLATE_PATH.read_text(encoding="utf-8")

@router.post("/ask", response_model=AgentResponse)
def ask_question(req: QuestionRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        state = run_agent(req.question)
        
        rejection = state.get("rejection_reason")
        if rejection:
            final_result = f"Result = Rejected, Reason: {rejection}"
        else:
            final_result = state.get("explained_result") or str(state.get("result"))
            print(final_result)

        return AgentResponse(
            result=final_result,
            valid_code=bool(state.get("valid_code")),
            error=state.get("error_message"),
            attempts=state.get("attempts", 0),
            explanation=state.get("explained_result")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")