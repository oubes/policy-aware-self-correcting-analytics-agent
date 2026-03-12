from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState
from scripts.graph_utils import save_graph_image
from app.graph.nodes import (
    get_question_node, build_prompt_node, ask_llm_node,
    fix_code_node, validate_code_node, extract_code_node, 
    run_code_node, explain_result_node
)
from app.graph.edges import (
    route_after_question, route_after_validate, route_after_run_code,
    route_after_extraction
)
def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("get_question", get_question_node)
    workflow.add_node("build_prompt", build_prompt_node)
    workflow.add_node("ask_llm", ask_llm_node)
    workflow.add_node("fix_code", fix_code_node)
    workflow.add_node("validate_code", validate_code_node)
    workflow.add_node("extract_code", extract_code_node)
    workflow.add_node("run_code", run_code_node)
    workflow.add_node("explain_result", explain_result_node)

    workflow.add_edge(START, "get_question")

    workflow.add_conditional_edges(
        "get_question",
        route_after_question,
        {"continue": "build_prompt", "reject": END}
    )

    workflow.add_edge("build_prompt", "ask_llm")
    workflow.add_edge("ask_llm", "validate_code")

    workflow.add_conditional_edges(
        "validate_code",
        route_after_validate,
        {
            "valid": "extract_code",
            "retry": "fix_code", # التعديل هنا: يروح يصلح لو الكود مخالف
            "invalid": END
        }
    )

    workflow.add_conditional_edges(
        "extract_code",
        route_after_extraction,
        {"continue": "run_code", "retry": "fix_code", "fail": END}
    )

    workflow.add_conditional_edges(
        "run_code",
        route_after_run_code,
        {"success": "explain_result", "retry": "fix_code", "fail": END}
    )

    workflow.add_edge("fix_code", "validate_code")
    workflow.add_edge("explain_result", END)

    return workflow.compile()

def run_agent(question: str) -> AgentState:
    initial_state: AgentState = {
        "question": question,
        "schema": {},
        "prompt": None,
        "raw_code": None,
        "extracted_code": None,
        "valid_code": None,
        "result": None,
        "explained_result": None,
        "authorized": None,
        "rejection_reason": None,
        "request_received": None,
        "request_classified": None,
        "analysis_done": None,
        "answered": None,
        "attempts": 0,
        "error_message": None
    }

    app = build_graph()
    save_graph_image(app)
    return app.invoke(initial_state)