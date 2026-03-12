from fastapi import APIRouter, HTTPException, Query
from app.graph.graph_builder import run_agent
from app.data.loader import load_dataset
from app.core.config import CSV_PATH, DEVICE
from app.agent.llm_client import ask_llm, client  # استخدم الـ API client بتاعك

router = APIRouter()

# Load dataset once at startup
df = load_dataset(CSV_PATH)

@router.get("/ask")
def ask_question(question: str = Query(..., description="User's analytics question")):
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        result = run_agent(
            question=question,
            df=df,
            client=client
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")

    return {"question": question, "answer": result}