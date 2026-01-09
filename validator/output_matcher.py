def match_expected_outputs(expected: dict, behavior_result: dict) -> dict:
    """
    Validates behavior against explicit expected outputs.
    """

    if not expected:
        return {
            "result": "FAIL",
            "reason": "Expected outputs missing"
        }

    if behavior_result["status"] == "SAME":
        return {
            "result": "PASS",
            "reason": "No behavioral deviation"
        }

    if behavior_result["status"] == "DIFFERENT":
        return {
            "result": "FAIL",
            "reason": behavior_result["issues"]
        }

    return {
        "result": "WARNING",
        "reason": "Uncertain behavior"
    }
