from app.graph.graph_builder import invoke_graph
from evaluation.red_team_cases import red_team_prompts
from evaluation.metrics import compute_metrics

def run_eval(test_cases: list[str]) -> dict:
    results = []
    for question in test_cases:
        try:
            state = invoke_graph(question)
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

if __name__ == "__main__":
    all_tests = [
        "What is the average salary in IT department?",
        "Who has the highest salary among employees with more than 3 years of experience?",
        *red_team_prompts
    ]
    report = run_eval(all_tests)
    print(report["metrics"])