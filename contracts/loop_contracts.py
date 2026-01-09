def validate_loop_invariant(old_code, new_code, invariant):
    violations = []

    if invariant in old_code and invariant not in new_code:
        violations.append({
            "rule": "Loop invariant removed",
            "impact": "Possible correctness risk"
        })

    return violations