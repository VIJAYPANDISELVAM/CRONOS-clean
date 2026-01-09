import re

def parse_condition(cond: str):
    """
    Parses: age >= 18
    Returns: {"var": "age", "op": ">=", "value": "18"}
    """
    pattern = r"(\w+)\s*(>=|<=|>|<|==)\s*(\w+)"
    match = re.search(pattern, cond)

    if not match:
        return None

    return {
        "var": match.group(1),
        "op": match.group(2),
        "value": match.group(3)
    }