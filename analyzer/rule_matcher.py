def match_rules(all_rules, target_variable):
    """
    Returns all rules that match the same variable
    """
    return [r for r in all_rules if r["variable"] == target_variable]
