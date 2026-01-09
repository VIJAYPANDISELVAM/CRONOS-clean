def calculate_risk(boundary_changed, test_case_count, variable):
    score = 0

    if boundary_changed:
        score += 30

    if test_case_count > 0:
        score += 40

    if variable in ["price", "interest"]:
        score += 20

    if score >= 76:
        level = "CRITICAL"
    elif score >= 51:
        level = "HIGH"
    elif score >= 21:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level
