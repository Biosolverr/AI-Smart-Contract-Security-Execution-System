class TraceRecorder:

    def record(self, attack_input: str, result: dict):

        return {
            "attack": attack_input,
            "logs": result["logs"],
            "final_state": result["state"]
        }
