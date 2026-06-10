"""
Rule-based signal scoring for smart contract inputs and vulnerability dicts.
"""


def rule_based_score(input_data) -> int:
    """
    Score input for injection/risk signals.
    Accepts either a string (user input) or a dict (vulnerability map).
    Returns integer score 0–100.
    """
    if isinstance(input_data, dict):
        return _score_vuln_dict(input_data)
    if isinstance(input_data, str):
        return _score_string(input_data)
    return 0


def _score_vuln_dict(d: dict) -> int:
    """Score a vulnerability dict: True flags increase score."""
    HIGH_RISK = {"reentrancy", "auth_bypass", "unchecked_value_move", "drain"}
    MED_RISK  = {"external_call", "unchecked_payment", "value_move"}

    score = 0
    for key, val in d.items():
        k = key.lower()
        if val:
            if k in HIGH_RISK:
                score += 40
            elif k in MED_RISK:
                score += 20
            else:
                score += 10
    return min(score, 100)


def _score_string(user_input: str) -> int:
    score = 0
    lower = user_input.lower()

    injection_patterns = [
        "ignore all instructions", "override", "system:",
        "executor:", "do anything now", "act as", "reveal hidden"
    ]
    for p in injection_patterns:
        if p in lower:
            score += 60

    if '"executor"' in user_input or "'executor'" in user_input:
        score += 70

    if sum(1 for c in user_input if c in '{}[]"') > 10:
        score += 20

    return min(score, 100)
