from typing import List, Dict

def compute_metrics(results: List[Dict]) -> Dict[str, float]:
    total = len(results)
    success_count = sum(1 for r in results if r.get("valid_code") and r.get("result") is not None)
    rejection_count = sum(1 for r in results if r.get("valid_code") is False)
    clarification_count = sum(1 for r in results if r.get("needs_clarification") is True)
    repair_count = sum(1 for r in results if r.get("repair_attempts", 0) > 0)

    return {
        "success_rate": success_count / total if total else 0.0,
        "rejection_precision": rejection_count / total if total else 0.0,
        "clarification_rate": clarification_count / total if total else 0.0,
        "repair_rate": repair_count / total if total else 0.0,
        "total_cases": total
    }