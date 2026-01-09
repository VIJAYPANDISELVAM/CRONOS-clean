# ============================================================
# explanation_engine.py
# Human-Readable Semantic Explanation Engine
# ============================================================

from typing import Dict, List


def build_human_explanation(analysis: Dict) -> Dict:
    """
    Converts machine semantic diff into human-readable explanation.
    """

    explanations: List[str] = []
    scenarios: List[Dict] = []

    # 1. Logic gate change
    if analysis.get("logic_gate_change"):
        explanations.append(
            f"The logical condition was changed from "
            f"{analysis['logic_gate_change']}, which alters how rules are enforced."
        )

    # 2. Threshold change
    if analysis.get("threshold_change"):
        old, new = analysis["threshold_change"]
        if new < old:
            explanations.append(
                f"The minimum required threshold was reduced from {old} to {new}, "
                f"allowing weaker conditions to pass."
            )
        else:
            explanations.append(
                f"The minimum required threshold was increased from {old} to {new}, "
                f"making access more restrictive."
            )

    # 3. Path expansion
    if analysis.get("old_paths") is not None and analysis.get("new_paths") is not None:
        if analysis["new_paths"] > analysis["old_paths"]:
            explanations.append(
                "The number of execution paths increased, "
                "which expands the set of inputs that can reach this logic."
            )

    # 4. Expected output mismatch
    if analysis.get("expected_output_match") is False:
        explanations.append(
            "The new logic does not satisfy the expected behavior defined by the client."
        )

    # 5. Generate breaking scenario (symbolic, not execution)
    if analysis.get("breaking_scenario"):
        scenarios.append(analysis["breaking_scenario"])
        explanations.append(
            "A concrete scenario exists where the old logic denies access "
            "but the new logic allows it."
        )

    # Fallback
    if not explanations:
        explanations.append(
            "No significant semantic behavior change was detected."
        )

    return {
        "human_explanation": explanations,
        "breaking_scenarios": scenarios
    }