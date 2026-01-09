def analyze_boolean(old_cond: str, new_cond: str):
    violations = []

    if "and" in old_cond and "or" in new_cond:
        violations.append({
            "rule": "Logical widening",
            "impact": "More users allowed"
        })

    if "or" in old_cond and "and" in new_cond:
        violations.append({
            "rule": "Logical narrowing",
            "impact": "More users blocked"
        })

    return violations