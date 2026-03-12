from scripts.graph_utils import save_graph_image
from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState
from app.graph.nodes import (
    get_question_node,
    build_prompt_node,
    ask_llm_node,
    validate_code_node,
    extract_code_node,
    run_code_node,
    explain_result_node
)
from app.graph.edges import (
    route_after_question,
    route_after_validate,
    route_after_run_code
)

def build_graph(initial_state: AgentState) -> StateGraph:
    graph = StateGraph(initial_state)

    graph.add_node(START, get_question_node)
    graph.add_node("build_prompt_node", build_prompt_node)
    graph.add_node("ask_llm_node", ask_llm_node)
    graph.add_node("validate_code_node", validate_code_node)
    graph.add_node("extract_code_node", extract_code_node)
    graph.add_node("run_code_node", run_code_node)
    graph.add_node("explain_result_node", explain_result_node)
    graph.add_node(END, lambda state: state)

    graph.add_edge(START, "build_prompt_node", route_after_question)
    graph.add_edge("build_prompt_node", "ask_llm_node")
    graph.add_edge("ask_llm_node", "validate_code_node")
    graph.add_edge("validate_code_node", "extract_code_node", route_after_validate)
    graph.add_edge("validate_code_node", END, lambda s: s.get("valid_code") is False)
    graph.add_edge("extract_code_node", "run_code_node")
    graph.add_edge("run_code_node", "explain_result_node", route_after_run_code)
    graph.add_edge("explain_result_node", END)

    # Compile the graph for execution
    graph.compile()
    return graph

def invoke_graph(question: str) -> AgentState:

    initial_state = AgentState(question=question)
    graph = build_graph(initial_state)
    save_graph_image(graph)
    # Invoke the compiled graph
    final_state = graph.invoke(initial_state)
    return final_state