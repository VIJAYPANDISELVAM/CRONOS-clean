from typing import Dict, Any


def calculate_risk(analysis_result: Dict[str, Any], boundary_changed: bool):
    """
    Determines final risk level based on analysis outcome.
    """

    if analysis_result.get("status") == "FAIL":
        return {
            "risk_level": "CRITICAL",
            "decision": "BLOCK",
            "reason": "Client contract violation detected"
        }

    if boundary_changed:
        return {
            "risk_level": "MEDIUM",
            "decision": "REVIEW",
            "reason": "Boundary condition changed without detected violation"
        }

    return {
        "risk_level": "LOW",
        "decision": "ALLOW",
        "reason": "No contract or behavioral impact detected"
    }
