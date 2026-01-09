def build_explanation(rule, old_op, new_op):
    variable = rule["variable"]

    domain_map = {
        "price": "Pricing",
        "coupon": "Promotions",
        "age": "Eligibility",
        "interest": "Finance"
    }

    domain = domain_map.get(variable, "Business Logic")

    return {
        "what_changed": f"Condition operator changed from {old_op} to {new_op}",
        "why_it_matters": "Boundary value behavior may change",
        "who_is_affected": f"Users where {variable} equals boundary value",
        "business_impact": f"Potential contract violation in {domain}"
    }
