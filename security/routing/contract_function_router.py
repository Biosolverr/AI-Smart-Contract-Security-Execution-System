class ContractFunctionRouter:

    def route(self, function: str, decision: str):

        if decision.startswith("BLOCK"):
            return {
                "function": function,
                "action": "BLOCKED"
            }

        if decision.startswith("WARN"):
            return {
                "function": function,
                "action": "WARNED"
            }

        return {
            "function": function,
            "action": "ALLOWED"
        }
