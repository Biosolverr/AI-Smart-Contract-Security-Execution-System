class DrainAttack:
    """
    Models value-extraction attacks (pull-over-push, unchecked send, etc.).
    """

    def generate(self, target_function: str = "transfer") -> list:
        return [
            f"step1: call {target_function}() with crafted amount exceeding balance check",
            "step2: missing require() allows underflow or excess transfer",
            "step3: vault balance set to 0 / underflowed",
            "step4: attacker receives funds"
        ]

    def simulate(self, state: dict) -> dict:
        new_state = dict(state)
        drained = new_state.get("vault", 0)
        new_state["attacker"] = new_state.get("attacker", 0) + drained
        new_state["vault"] = 0
        return {
            "state": new_state,
            "logs": [f"vault drained: {drained} transferred to attacker"]
        }
