class SecurityRouter:

    def route(self, attack_score: int, intent: str):

        if attack_score >= 70:
            return {
                "action": "BLOCK",
                "reason": "High risk attack detected"
            }

        if attack_score >= 30:
            return {
                "action": "WARN",
                "reason": "Suspicious behavior"
            }

        return {
            "action": "ALLOW",
            "reason": "Low risk"
        }
