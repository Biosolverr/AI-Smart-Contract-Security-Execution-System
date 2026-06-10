class AuthBypassAttack:
    """
    Models access-control bypass attempts.
    """

    def generate(self, target_function: str = "setOwner") -> list:
        return [
            f"step1: identify {target_function}() has no onlyOwner modifier",
            "step2: call from attacker address directly",
            f"step3: {target_function}() executes — ownership/privilege escalated",
            "step4: attacker now controls privileged state"
        ]

    def simulate(self, state: dict) -> dict:
        new_state = dict(state)
        new_state["owner"] = "attacker"
        return {
            "state": new_state,
            "logs": ["onlyOwner check absent", "owner overwritten to attacker"]
        }
