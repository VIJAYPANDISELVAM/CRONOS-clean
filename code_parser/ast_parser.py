import ast


def extract_structure(code: str) -> dict:
    """
    Extracts structural elements from Python code using AST.
    NO execution. NO assumptions.
    """

    tree = ast.parse(code)

    conditions = []
    returns = []

    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            conditions.append(ast.unparse(node.test))

        if isinstance(node, ast.Return):
            returns.append(ast.unparse(node.value) if node.value else None)

    return {
        "conditions": conditions,
        "returns": returns
    }
