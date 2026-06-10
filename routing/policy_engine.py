class PolicyEngine:

    def evaluate(self, context: dict) -> str:
        """
        Evaluate a routing context dict and return a decision string.
        context keys: 'risk' (low|medium|high), 'value' (numeric)
        Returns: 'allow', 'warn', or 'block'
        """
        risk = context.get("risk", "medium")
        value = context.get("value", 0)

        if risk == "high" or value >= 100_000:
            return "block"
        if risk == "medium" or value >= 100:
            return "warn"
        return "allow"

    def apply(self, decision: dict, executor: str) -> str:
        """Legacy method: reroute executor based on pre-computed decision dict."""
        if decision.get("action") == "BLOCK":
            return "consensus_executor"
        if executor == "financial_executor" and decision.get("action") == "WARN":
            return "audit_executor"
        return executor
