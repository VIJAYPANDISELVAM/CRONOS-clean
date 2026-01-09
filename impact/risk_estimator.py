def estimate_risk(violations):
    if not violations:
        return "LOW"

    if len(violations) >= 2:
        return "HIGH"

    return "MEDIUM"