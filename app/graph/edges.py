from app.graph.state import AgentState

def route_after_question(state: AgentState) -> str:
    if state.get("authorized") is False:
        return "reject"
    return "continue"

def route_after_validate(state: AgentState) -> str:
    if state.get("valid_code") is True:
        return "valid"
    
    if state.get("attempts", 0) < 3:
        return "retry"
    
    return "invalid" 

def route_after_run_code(state: AgentState) -> str:
    if state.get("error_message") is None:
        return "success"
    
    if state.get("attempts", 0) < 3:
        return "retry"
    
    return "fail"

def route_after_extraction(state: AgentState) -> str:
    if state.get("extracted_code") and state["extracted_code"].strip():
        return "continue"
    
    if state.get("attempts", 0) < 3:
        return "retry"
    
    return "fail"