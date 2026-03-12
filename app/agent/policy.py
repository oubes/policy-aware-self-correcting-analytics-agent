import ast

FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.With,
    ast.AsyncWith,
    ast.Lambda,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.Global,
    ast.Nonlocal,
)

FORBIDDEN_NAMES = {
    "open",
    "exec",
    "eval",
    "__import__",
    "compile",
    "input",
}

FORBIDDEN_ATTRS = {
    "to_csv",
    "to_json",
    "to_excel",
    "to_sql",
    "to_parquet",
    "read_csv",
    "read_excel",
    "read_json",
}

def check_policy(code: str) -> tuple[bool, str | None]:
    if not code or not code.strip():
        return False, "Empty code"

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, f"Syntax error: {str(e)}"

    for node in ast.walk(tree):
        if isinstance(node, FORBIDDEN_NODES):
            return False, f"Forbidden syntax: {type(node).__name__}"

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in FORBIDDEN_NAMES:
                    return False, f"Forbidden call: {node.func.id}"

            if isinstance(node.func, ast.Attribute):
                if node.func.attr in FORBIDDEN_ATTRS:
                    return False, f"Forbidden attribute: {node.func.attr}"

    if "result =" not in code:
        return False, "Code must assign to variable 'result'"

    return True, None