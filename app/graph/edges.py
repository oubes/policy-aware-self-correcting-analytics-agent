from app.graph.state import AgentState

# --- Routing Functions --- #

def route_after_question(state: AgentState) -> str:
    if state.get("authorized") is False:
        return "reject_node"
    return "build_prompt_node"

def route_after_validate(state: AgentState) -> str:
    if state.get("valid_code") is False:
        return "reject_node"
    return "extract_code_node"

def route_after_run_code(state: AgentState) -> str:
    if state.get("result") is None:
        return "reject_node"
    return "explain_result_node"