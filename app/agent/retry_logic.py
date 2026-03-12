from app.agent.llm_client import ask_llm
from app.agent.prompts import REPAIR_PROMPT

def ask_llm_to_fix(schema: dict, question: str, code: str | None, error: str | None) -> str:
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