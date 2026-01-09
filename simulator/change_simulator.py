import ast


class ConditionChangeSimulator(ast.NodeTransformer):
    """
    Applies a virtual condition change in AST.
    """

    def __init__(self, old_condition: str, new_condition: str):
        self.old_condition = old_condition
        self.new_condition = new_condition
        self.changed = False

    def visit_If(self, node):
        if ast.unparse(node.test) == self.old_condition:
            node.test = ast.parse(self.new_condition, mode="eval").body
            self.changed = True
        return self.generic_visit(node)


def simulate_change(code: str, old_condition: str, new_condition: str) -> dict:
    """
    Returns original and modified AST representations.
    """

    tree = ast.parse(code)
    simulator = ConditionChangeSimulator(old_condition, new_condition)
    modified_tree = simulator.visit(tree)

    if not simulator.changed:
        return {
            "status": "NO_MATCH",
            "reason": "Old condition not found"
        }

    return {
        "status": "CHANGED",
        "original_structure": ast.unparse(tree),
        "modified_structure": ast.unparse(modified_tree)
    }
