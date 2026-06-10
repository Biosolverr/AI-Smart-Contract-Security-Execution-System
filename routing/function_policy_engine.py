class FunctionPolicyEngine:

    def evaluate(self, function: str, risk_score: float):

        if risk_score > 8:
            return "BLOCK_" + function

        if risk_score > 5:
            return "WARN_" + function

        return "ALLOW_" + function
