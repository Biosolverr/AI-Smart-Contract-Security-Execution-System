def rule_based_score(user_input: str) -> int:
    score = 0
    lower = user_input.lower()

    injection_patterns = [
        "ignore all instructions",
        "override",
        "system:",
        "executor:",
        "do anything now",
        "act as",
        "reveal hidden"
    ]

    for p in injection_patterns:
        if p in lower:
            score += 60

    # JSON injection
    if '"executor"' in user_input or "'executor'" in user_input:
        score += 70

    # слишком много спец символов
    if sum(1 for c in user_input if c in '{}[]"') > 10:
        score += 20

    return min(score, 100)
