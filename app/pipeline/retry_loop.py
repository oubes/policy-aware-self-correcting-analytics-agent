from app.agent.llm_client import ask_llm
from app.execution.executor import run_code
from app.agent.prompts import build_prompt, REPAIR_PROMPT

def ask_llm_to_fix(schema: dict, question: str, code: str, error: str) -> str:
    prompt = f"""
{REPAIR_PROMPT}

Schema:
{schema}

Question:
{question}

Broken Code:
{code}

Error:
{error}

Return fixed code:
"""
    return ask_llm([{"role": "user", "content": prompt}])

def execute_with_retry(question: str, df, max_retries: int = 2):
    schema = {
        "columns": list(df.columns),
        "rows": len(df)
    }

    # First code generation
    code = ask_llm([{"role": "user", "content": build_prompt(question, schema)}])

    for attempt in range(max_retries):
        try:
            result = run_code(code, df)
            return result

        except Exception as e:
            if attempt == max_retries - 1:
                return "I could not compute this safely. Try rephrasing."

            code = ask_llm_to_fix(schema, question, code, str(e))