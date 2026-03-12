from app.graph.state import AgentState
from app.agent.prompts import build_prompt
from app.agent.llm_client import ask_llm, ask_llm_to_fix
from app.agent.code_cleaner import clean_llm_code
from app.execution.executor import run_code
from app.agent.policy import check_policy
from app.data.loader import load_dataset

df = load_dataset()

# --- Nodes --- #

def get_question_node(state: AgentState) -> AgentState:
    # Mark that a question was received
    state["request_received"] = True
    return state

def build_prompt_node(state: AgentState) -> AgentState:
    # Build LLM prompt based on question and schema
    state["prompt"] = build_prompt(state["question"], state["schema"])
    return state

def ask_llm_node(state: AgentState) -> AgentState:
    # Ask the LLM to generate code
    state["raw_code"] = ask_llm([{"role": "user", "content": state["prompt"]}])
    return state

def validate_code_node(state: AgentState) -> AgentState:
    # Validate code policy (aggregated-only, no forbidden operations)
    try:
        check_policy(state["raw_code"])
        state["valid_code"] = True
    except ValueError as e:
        state["valid_code"] = False
        state["rejection_reason"] = str(e)
    return state

def extract_code_node(state: AgentState) -> AgentState:
    # Extract valid python from LLM output
    state["extracted_code"] = clean_llm_code(state["raw_code"])
    return state

def run_code_node(state: AgentState) -> AgentState:
    # Execute the code safely and store the result
    state["result"] = run_code(state["extracted_code"], df)
    state["analysis_done"] = True
    return state

def explain_result_node(state: AgentState) -> AgentState:
    # Simple explanation layer
    state["explained_result"] = f"Result: {state['result']}"
    return state