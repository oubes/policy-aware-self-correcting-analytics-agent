from app.graph.state import AgentState
from app.agent.explain_result import sanitize_output
from app.agent.prompts import build_prompt
from app.agent.llm_client import ask_llm
from app.agent.retry_logic import ask_llm_to_fix
from app.agent.code_cleaner import clean_llm_code
from app.execution.executor import run_code
from app.agent.policy import check_policy
from app.data.loader import load_dataset

df = load_dataset()

def get_question_node(state: AgentState) -> AgentState:
    state["request_received"] = True
    if state.get("authorized") is None:
        state["authorized"] = True
    
    state["schema"] = {
        "columns": list(df.columns),
        "rows": len(df)
    }
    return state

def build_prompt_node(state: AgentState) -> AgentState:
    state["prompt"] = build_prompt(state["question"], state["schema"])
    return state

def ask_llm_node(state: AgentState) -> AgentState:
    state["raw_code"] = ask_llm([{"role": "user", "content": state["prompt"]}])
    print("LLM raw response:\n", state["raw_code"])
    return state

def fix_code_node(state: AgentState) -> AgentState:
    print("Attempting to fix code. Current error message:", state.get("error_message"))
    state["raw_code"] = ask_llm_to_fix(
        state["schema"],
        state["question"],
        state["raw_code"],
        state["error_message"]
    )
    return state

def validate_code_node(state: AgentState) -> AgentState:
    raw_code = state.get("raw_code", "")
    is_valid, error_msg = check_policy(raw_code)
    
    if is_valid:
        state["valid_code"] = True
        state["rejection_reason"] = None
        state["error_message"] = None # Added to clear any previous errors
    else:
        state["valid_code"] = False
        state["rejection_reason"] = error_msg
        state["error_message"] = f"Policy Violation: {error_msg}"
        state["attempts"] = state.get("attempts", 0) + 1 
        
    return state

def extract_code_node(state: AgentState) -> AgentState:
    print("Raw code from LLM:\n", state.get("raw_code"))
    cleaned = clean_llm_code(state["raw_code"])
    state["extracted_code"] = cleaned
    
    if not cleaned or cleaned.strip() == "":
        state["error_message"] = "Failed to extract any valid Python code from the LLM response."
        state["attempts"] = state.get("attempts", 0) + 1
        print("attempts after failed extraction:", state["attempts"])
    else:
        state["error_message"] = None # Added to clear any previous errors
    
    return state

def run_code_node(state: AgentState) -> AgentState:
    print("Executing code:\n", state.get("extracted_code"))
    try:
        state["result"] = run_code(state["extracted_code"], df)
        state["analysis_done"] = True
        state["error_message"] = None
    except Exception as e:
        state["result"] = None
        state["error_message"] = str(e)
        state["attempts"] = state.get("attempts", 0) + 1
        print("attempts after failed execution:", state["attempts"])
    return state

def explain_result_node(state: AgentState) -> AgentState:
    clean_result = sanitize_output(state.get("result"))
    state["result"] = clean_result
    state["explained_result"] = f"Result: {clean_result}"
    state["answered"] = True
    return state