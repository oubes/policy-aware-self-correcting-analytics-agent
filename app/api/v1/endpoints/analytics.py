from fastapi import APIRouter, HTTPException
from app.graph.graph_builder import run_agent
from app.api.schemas import QuestionRequest, AgentResponse 

router = APIRouter()


@router.post("/ask", response_model=AgentResponse)
def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        state = run_agent(question=request.question)
        
        if state.get("rejection_reason"):
            final_result = f"Result = Rejected, Reason: {state.get('rejection_reason')}"
        else:
            final_result = state.get("explained_result") or state.get("result")

        return AgentResponse(
            result=final_result,
            valid_code=bool(state.get("valid_code")),
            error=state.get("error_message"),
            attempts=state.get("attempts", 0),
            explanation=state.get("rejection_reason")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")