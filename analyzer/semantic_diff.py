def analyze_direction(old, new):
    violations = []

    if old["var"] != new["var"]:
        violations.append({
            "rule": "Variable changed",
            "impact": "Logic target modified"
        })

    direction_map = {
        ">": "gt",
        ">=": "gt",
        "<": "lt",
        "<=": "lt",
        "==": "eq"
    }

    if direction_map.get(old["op"]) != direction_map.get(new["op"]):
        violations.append({
            "rule": "Condition direction reversed",
            "impact": "Accept ↔ Reject logic inverted"
        })

    return violations