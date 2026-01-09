def compute_confidence(expected, detected, boundary_changed):
    score = 100

    if boundary_changed:
        score -= 40

    if expected != detected:
        score -= 40

    return max(score, 0)
