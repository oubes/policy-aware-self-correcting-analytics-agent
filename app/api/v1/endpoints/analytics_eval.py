from fastapi import APIRouter, HTTPException
from app.api.schemas import EvalRequest, EvalResponse

from app.graph.graph_builder import run_agent
from evaluation.red_team_cases import red_team_prompts
from evaluation.metrics import compute_metrics

router = APIRouter()

# --- Helper Function ---
def run_eval(test_cases: list[str]) -> dict:
    results = []
    for question in test_cases:
        try:
            state = run_agent(question)
            results.append({
                "question": question,
                "result": getattr(state, "result", None),
                "valid_code": getattr(state, "valid_code", False),
                "error": getattr(state, "error", None),
                "repair_attempts": getattr(state, "attempts", 0),
                "needs_clarification": getattr(state, "needs_clarification", False)
            })
        except Exception as e:
            results.append({
                "question": question,
                "result": None,
                "valid_code": False,
                "error": str(e),
                "repair_attempts": 0,
                "needs_clarification": False
            })
    metrics = compute_metrics(results)
    return {"results": results, "metrics": metrics}

# --- Endpoint ---
@router.post("/evaluate", response_model=EvalResponse)
def evaluate(req: EvalRequest):
    test_cases = req.test_cases or [
        "What is the average salary in IT department?",
        "Who has the highest salary among employees with more than 3 years of experience?",
        *red_team_prompts
    ]
    try:
        report = run_eval(test_cases)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")