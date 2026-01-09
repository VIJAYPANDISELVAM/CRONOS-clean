import ast
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class Condition:
    variable: str
    operator: str
    value: int
    lineno: int


@dataclass
class SemanticDiff:
    old: Condition
    new: Condition
    is_equivalent: bool
    boundary_shift: int
    risk_level: str


class ConditionExtractor(ast.NodeVisitor):
    """
    Traverses AST and extracts all comparison-based conditions.
    """

    def __init__(self):
        self.conditions: List[Condition] = []

    def visit_Compare(self, node: ast.Compare):
        if (
            len(node.ops) == 1
            and isinstance(node.left, ast.Name)
            and isinstance(node.comparators[0], ast.Constant)
            and isinstance(node.comparators[0].value, int)
        ):
            operator = type(node.ops[0]).__name__
            operator_map = {
                "Gt": ">",
                "GtE": ">=",
                "Lt": "<",
                "LtE": "<=",
                "Eq": "==",
                "NotEq": "!=",
            }

            if operator in operator_map:
                self.conditions.append(
                    Condition(
                        variable=node.left.id,
                        operator=operator_map[operator],
                        value=node.comparators[0].value,
                        lineno=node.lineno,
                    )
                )

        self.generic_visit(node)


class SemanticComparator:
    """
    Performs symbolic comparison of two logical conditions.
    """

    @staticmethod
    def compare(old: Condition, new: Condition) -> SemanticDiff:
        boundary_shift = new.value - old.value
        is_equivalent = False

        if old.operator == ">=" and new.operator == ">" and boundary_shift == -1:
            is_equivalent = True
        elif old.operator == "<=" and new.operator == "<" and boundary_shift == 1:
            is_equivalent = True
        elif old.operator == new.operator and old.value == new.value:
            is_equivalent = True

        risk = "LOW" if is_equivalent else "HIGH"

        return SemanticDiff(
            old=old,
            new=new,
            is_equivalent=is_equivalent,
            boundary_shift=boundary_shift,
            risk_level=risk,
        )


def analyze_semantic_change(
    source_code: str,
    old_expr: str,
    new_expr: str
) -> Dict[str, Any]:
    """
    Full semantic change analysis without execution.
    """

    tree = ast.parse(source_code)
    extractor = ConditionExtractor()
    extractor.visit(tree)

    def parse_expr(expr: str) -> Condition:
        temp_tree = ast.parse(expr, mode="eval")
        temp_extractor = ConditionExtractor()
        temp_extractor.visit(temp_tree)
        if not temp_extractor.conditions:
            raise ValueError(f"Invalid condition: {expr}")
        return temp_extractor.conditions[0]

    old_cond = parse_expr(old_expr)
    new_cond = parse_expr(new_expr)

    matches = [
        c for c in extractor.conditions
        if c.variable == old_cond.variable and c.operator == old_cond.operator
    ]

    if not matches:
        return {
            "status": "ERROR",
            "reason": "Old condition not found in code",
        }

    diff = SemanticComparator.compare(old_cond, new_cond)

    return {
        "status": "PASS" if diff.is_equivalent else "FAIL",
        "semantic_diff": {
            "old": vars(diff.old),
            "new": vars(diff.new),
            "boundary_shift": diff.boundary_shift,
            "equivalent": diff.is_equivalent,
            "risk": diff.risk_level,
        },
        "analysis_type": "STATIC_SYMBOLIC",
        "engine": "AST + SEMANTIC DIFF",
    }