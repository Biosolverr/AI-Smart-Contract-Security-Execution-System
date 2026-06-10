class ReentrancyAttack:
    """
    Models a reentrancy exploit chain.
    Generates step-by-step attack sequence for simulation.
    """

    def generate(self, target_function: str = "withdraw") -> list:
        return [
            f"step1: call {target_function}() from attacker contract",
            f"step2: attacker fallback() re-enters {target_function}() before state update",
            "step3: repeat recursively until vault is drained",
            "step4: state update finally executes with zero balance"
        ]

    def simulate(self, state: dict, drain_amount: int = 1000) -> dict:
        logs = []
        new_state = dict(state)
        while new_state.get("vault", 0) >= drain_amount:
            new_state["vault"] -= drain_amount
            new_state["attacker"] = new_state.get("attacker", 0) + drain_amount
            logs.append(f"re-entered: drained {drain_amount}, vault={new_state['vault']}")
        return {"state": new_state, "logs": logs}
