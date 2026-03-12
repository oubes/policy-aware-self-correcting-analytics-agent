REPAIR_PROMPT = """
You are a pandas debugger.

Fix the code based on the error.

Rules:
- Return ONLY corrected python code.
- No explanations.
- No imports.
- Must assign result variable.
"""

def build_prompt(question: str, schema: dict) -> str:
    return f"""
You are a pandas data analyst.

Write executable pandas code to answer the question.

Rules:
- Use ONLY existing dataframe columns.
- No explanations.
- No markdown.
- No imports.
- Must assign final answer to variable: result.

Schema:
{schema}

Question:
{question}
"""