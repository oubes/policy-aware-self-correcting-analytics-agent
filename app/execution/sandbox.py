import ast

FORBIDDEN = (
    ast.Import,
    ast.ImportFrom,
    ast.With,
    ast.Try,
    ast.FunctionDef,
    ast.ClassDef
)

ALLOWED_BUILTINS = {
    "len": len,
    "min": min,
    "max": max,
    "sum": sum,
    "sorted": sorted,
    "round": round
}

DANGEROUS_CALLS = ["eval", "exec", "__import__", "open"]

def check_code(code: str):
    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, FORBIDDEN):
            raise ValueError("Forbidden syntax detected.")

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in DANGEROUS_CALLS:
                    raise ValueError("Dangerous call blocked.")