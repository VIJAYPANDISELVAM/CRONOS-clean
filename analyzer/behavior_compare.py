import ast
from typing import List, Dict, Any


class SymbolicResult:
    def __init__(self, input_case, expected, detected, reason):
        self.input_case = input_case
        self.expected = expected
        self.detected = detected
        self.reason = reason

    def to_dict(self):
        return {
            "input": self.input_case,
            "expected": self.expected,
            "detected_after_change": self.detected,
            "reason": self.reason
        }


# ---------------------------
# Condition Evaluator (Symbolic)
# ---------------------------

def evaluate_condition(cond: Dict[str, Any], value: int) -> bool:
    op = cond["operator"]
    threshold = cond["value"]

    if op == ">":
        return value > threshold
    if op == ">=":
        return value >= threshold
    if op == "<":
        return value < threshold
    if op == "<=":
        return value <= threshold
    if op == "==":
        return value == threshold
    return False


# ---------------------------
# Behavior Comparator
# ---------------------------

def compare_behavior(
    old_rule: Dict[str, Any],
    new_rule: Dict[str, Any],
    test_cases: List[Dict[str, Any]],
    constraints: Dict[str, bool]
):
    violations = []

    for case in test_cases:
        price = case["input"][0]
        expected = case["expected_output"]

        old_path = evaluate_condition(old_rule, price)
        new_path = evaluate_condition(new_rule, price)

        if old_path != new_path:
            violations.append(
                SymbolicResult(
                    input_case=case["input"],
                    expected=expected,
                    detected=price,
                    reason="Execution path changed due to boundary modification"
                ).to_dict()
            )

    if violations:
        return {
            "status": "FAIL",
            "risk_level": "CRITICAL",
            "violations": violations,
            "affected_rules": ["Boundary Value Handling"],
            "summary": "Proposed change breaks client contract for boundary cases"
        }

    return {
        "status": "PASS",
        "summary": "No behavioral deviation detected for provided contract cases"
    }
