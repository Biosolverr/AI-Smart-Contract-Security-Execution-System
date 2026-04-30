class PolicyEngine:

    def apply(self, decision: dict, executor: str):

        if decision["action"] == "BLOCK":
            return "consensus_executor"

        if executor == "financial_executor" and decision["action"] == "WARN":
            return "audit_executor"

        return executor
