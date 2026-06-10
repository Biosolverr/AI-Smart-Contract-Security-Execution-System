def routing_policy(score: int):
    if score < 30:
        return {
            "mode": "execute",
            "confidence_cap": 100,
            "require_consensus": False
        }

    if score < 70:
        return {
            "mode": "guarded_execute",
            "confidence_cap": 60,
            "require_consensus": True,
            "require_confirmation": True
        }

    return {
        "mode": "blocked",
        "confidence_cap": 0,
        "audit_only": True
    }
