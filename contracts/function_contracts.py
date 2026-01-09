def validate_function_contract(old_cond, new_cond, contract):
    violations = []

    if contract["input"] in old_cond and contract["input"] not in new_cond:
        violations.append({
            "rule": "Contract violation",
            "impact": "Function input guarantee removed"
        })

    return violations