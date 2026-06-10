class SecurityGatekeeper:

    def enforce(self, routing_result: dict):

        if routing_result["action"] == "BLOCKED":
            return False

        return True
