from typing import Any
import pandas as pd
from app.execution.sandbox import check_code, ALLOWED_BUILTINS

def run_code(code: str, df: pd.DataFrame) -> Any:
    code = code.strip()

    check_code(code)

    safe_globals: dict[str, Any] = {
        "__builtins__": ALLOWED_BUILTINS,
        "pd": pd,
        "df": df
    }

    safe_locals: dict[str, Any] = {}

    exec(code, safe_globals, safe_locals)

    if "result" not in safe_locals:
        raise ValueError("Code must assign result")

    return safe_locals["result"]