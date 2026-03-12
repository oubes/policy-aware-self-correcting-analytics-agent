import re

def clean_llm_code(raw_code: str) -> str:
    if raw_code is None:
        return ""

    code = raw_code.strip()

    fence_pattern = r"```(?:python)?\s*(.*?)```"
    match = re.search(fence_pattern, code, re.DOTALL)

    if match:
        code = match.group(1).strip()

    lines = code.splitlines()

    cleaned_lines = []
    for line in lines:
        if line.strip().startswith("import"):
            continue
        if line.strip().startswith("from"):
            continue
        cleaned_lines.append(line)

    cleaned_code = "\n".join(cleaned_lines).strip()

    return cleaned_code