def analyze_range(old, new):
    violations = []

    if old["op"] == ">=" and new["op"] == ">":
        violations.append({
            "rule": "Boundary tightened",
            "impact": "Equality case removed"
        })

    if old["op"] == "<=" and new["op"] == "<":
        violations.append({
            "rule": "Boundary tightened",
            "impact": "Upper boundary excluded"
        })

    return violations